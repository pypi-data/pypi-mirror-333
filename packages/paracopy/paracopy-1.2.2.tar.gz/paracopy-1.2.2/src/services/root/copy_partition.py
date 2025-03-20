"""Script to copy source to multiple destinations.

Copyright (c) 2024 Pierre-Yves Genest.

This file is part of ParaCopy.

ParaCopy is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, version 3 of the
License.

ParaCopy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with ParaCopy. If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import contextlib
import functools
import os
import re
import subprocess
import sys
import time
from collections.abc import Callable
from pathlib import Path
from subprocess import DEVNULL, PIPE
from threading import Thread

from model.script import DeviceCopyMessage, ErrorMessage, SuccessMessage
from model.source import Source
from services.root.utils import (
    _,
    exit_with_error,
    exit_with_success,
    send_device_copy_message,
    send_progress,
)
from services.usb import UsbSizeService

NUM_WRITTEN_MBS_EXTRACTOR = re.compile("^([0-9]+) blocks")


class CopyWorker(Thread):
    """Worker for copy."""

    def __init__(
        self,
        source_path: str,
        block_ids: list[str],
        num_written_mbs_callback: Callable[[int], None],
        callback: Callable[[bool], None],
    ) -> None:
        """Construct CopyWorker.

        Args:
        ----
            source_path (str): absolute path to source
            block_ids (List[str]): block ids to copy
            num_written_mbs_callback (Callable[[int], None]): callback to transmit
                progress
            callback (Callable[[bool], None]): callback when copy is finished

        """
        super().__init__()
        self.source_path = source_path
        self.block_ids = block_ids
        self.num_written_mbs_callback = num_written_mbs_callback
        self.callback = callback

    def run(self) -> None:
        """Run copy."""
        last_num_written_mbs = 0

        with subprocess.Popen(
            [
                "/usr/bin/dcfldd",
                "bs=1M",
                "statusinterval=1",
                "status=on",
                f"if={Path(self.source_path).resolve()}/source.img",
                *[f"of=/dev/{dest}" for dest in self.block_ids],
            ],
            stderr=PIPE,
            stdout=DEVNULL,
            universal_newlines=True,
        ) as proc:
            # Parse number of written blocks
            for line in iter(proc.stderr.readline, ""):
                num_written_mbs = NUM_WRITTEN_MBS_EXTRACTOR.search(line)
                if num_written_mbs:
                    num_written_mbs = int(num_written_mbs.group(1))
                    if num_written_mbs - last_num_written_mbs >= 1:
                        self.num_written_mbs_callback(num_written_mbs)
                    last_num_written_mbs = num_written_mbs

            proc.communicate()

            # Parse error code
            self.callback(proc.returncode == 0)


class DirtyWritebackWorker(Thread):
    """Worker to monitor Dirty/Writeback memory."""

    def __init__(
        self,
        dirty_writeback_callback: Callable[[int], None],
    ) -> None:
        """Build DirtyWritebackWorker.

        Args:
        ----
            dirty_writeback_callback (Callable[[int], None]): to send progress back

        """
        super().__init__()
        self.dirty_writeback_callback = dirty_writeback_callback
        self.stop = False

    def ask_stop(self) -> None:
        """Ask to stop worker."""
        self.stop = True

    def run(self) -> None:
        """Run worker."""
        last_dirty_writeback = float("inf")
        while not self.stop:
            time.sleep(5)

            dirty = 0
            writeback = 0
            with Path("/proc/meminfo").open(encoding="utf-8") as file:
                for line in file:
                    if line.startswith("Dirty:"):
                        dirty = int(line.split()[1])
                    if line.startswith("Writeback:"):
                        writeback = int(line.split()[1])
                        break
            dirty_writeback = (dirty + writeback) / 1024

            if abs(last_dirty_writeback - dirty_writeback) >= 1:
                self.dirty_writeback_callback(dirty_writeback)
                last_dirty_writeback = dirty_writeback


class CopyProcess:
    """Overall scheduler of the copy process."""

    def __init__(self, args: dict) -> int:
        """Build CopyProcess.

        Args:
        ----
            args (dict): args

        """
        self.destination_block_ids = args.destination_block_id
        self.source_path = args.source_path
        with Path(f"{self.source_path}/metadata.json").open(
            encoding="utf-8",
        ) as file:
            self.source_metadata = Source.model_validate_json(file.read())

        self.num_destinations_per_process = args.num_destinations_per_process
        if self.num_destinations_per_process == 0:
            self.num_destinations_per_process = len(self.destination_block_ids)

        self.usb_size_service = UsbSizeService()

        # Copy model
        self.total_mbs_to_write = self.source_metadata.size
        self.dirty_writeback_mbs: float = float("inf")
        self.written_mbs: list[int] = []
        self.copy_workers: list[dict] = []

        self.devices_error: bool = False

    def copy_written_mbs_callback(self, index: int, written_mbs: int) -> None:
        """Handle progress coming from one of the copy workers.

        Args:
        ----
            index (int): index of worker
            written_mbs (int): written mbs

        """
        self.written_mbs[index] = written_mbs

    def copy_callback(self, index: int, success: int) -> None:
        """Handle end signal coming from one of the copy workers.

        Args:
        ----
            index (int): index of worker
            success (int): if copy is a success or an error

        """
        self.copy_workers[index]["finished"] = True
        destinations = self.copy_workers[index]["destinations"]
        for destination in destinations:
            self.check_copy(destination, success)

        if not success:
            self.devices_error = True

    def dirty_writeback_callback(self, new_dirty_writeback_mbs: int) -> None:
        """Handle progress coming from the dirty/writeback worker.

        Args:
        ----
            new_dirty_writeback_mbs (int): dirty/writeback amount

        """
        self.dirty_writeback_mbs = new_dirty_writeback_mbs / len(
            self.destination_block_ids,
        )

    def check_copy(self, block_id: str, process_success: int) -> None:
        """Check copy of destination.

        Args:
        ----
            block_id (str): destination (e.g., sda, sdb, ...)
            process_success (int): whether copy process was a success or not

        """
        occupied_space = self.usb_size_service.compute_occupied_space(block_id)

        send_device_copy_message(
            DeviceCopyMessage(
                block_id=block_id,
                success=process_success & occupied_space != -1,
                occupied_space=occupied_space,
            ),
        )

    def run(self) -> int:
        """Run copy.

        Returns
        -------
            int: return code

        """
        # Check parameter values
        if self.num_destinations_per_process < 0:
            return exit_with_error(
                ErrorMessage(
                    message=_(
                        "The number of destinations per copy process cannot be "
                        "negative.",
                    ),
                ),
            )

        if len(self.destination_block_ids) == 0 or any(
            not Path(f"/dev/{dest}").exists() for dest in self.destination_block_ids
        ):
            return exit_with_error(
                ErrorMessage(message=_("Error with the destinations.")),
            )

        if not Path(self.source_path).exists():
            return exit_with_error(ErrorMessage(message=_("Source does not exist.")))

        # Ensure user is root
        if os.geteuid() != 0:
            return exit_with_error(ErrorMessage(message=_("Insufficient permissions.")))

        # Create copy workers
        for i in range(
            0,
            len(self.destination_block_ids),
            self.num_destinations_per_process,
        ):
            current_block_ids = self.destination_block_ids[
                i : i + self.num_destinations_per_process
            ]
            current_worker = CopyWorker(
                self.source_path,
                current_block_ids,
                functools.partial(self.copy_written_mbs_callback, i),
                functools.partial(self.copy_callback, i),
            )
            self.copy_workers.append(
                {
                    "destinations": current_block_ids,
                    "worker": current_worker,
                    "finished": False,
                },
            )
            self.written_mbs.append(0)
            current_worker.start()

        # Create dirty writeback worker
        dirty_writeback_worker = DirtyWritebackWorker(self.dirty_writeback_callback)
        dirty_writeback_worker.start()

        # Monitor copy
        finished = False
        last_progress = 0
        send_progress(0)
        while not finished:
            finished = all(w["finished"] for w in self.copy_workers)

            written_mbs = float(sum(self.written_mbs) / len(self.written_mbs))
            progress = (
                max(0, written_mbs - self.dirty_writeback_mbs) / self.total_mbs_to_write
            )

            if progress - last_progress >= 0.01:
                send_progress(progress)
                last_progress = progress

            time.sleep(5)

        # Wait to finish device sync (to ensure everything is written on disk)
        with contextlib.suppress(Exception):
            subprocess.check_output(["/usr/bin/sync"])

        # Stop thread
        dirty_writeback_worker.ask_stop()
        for worker in self.copy_workers:
            worker["worker"].join()
        dirty_writeback_worker.join()

        send_progress(1)
        if self.devices_error:
            return exit_with_error(
                ErrorMessage(message=_("There were errors for some destinations.")),
            )

        return exit_with_success(SuccessMessage())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ParaCopy Copy Partition",
        description="Root script of ParaCopy to copy partition",
    )
    parser.add_argument(
        "--source-path",
        help="Path to source image (e.g., ~/.paracopy/sources/...)",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--destination-block-id",
        help="Destination of copy (e.g., sda, sdb)",
        action="append",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--num-destinations-per-process",
        help="Number of destinations per copy process",
        type=int,
        required=True,
    )
    parser_args = parser.parse_args()

    process = CopyProcess(parser_args)
    return_code = process.run()
    sys.exit(return_code)
