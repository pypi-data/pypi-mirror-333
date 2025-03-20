"""Services for source.

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

import asyncio
import math
import os
import re
import shutil
import sys
from collections.abc import Callable
from pathlib import Path

import pyudev
from localization import _
from model.source import Source
from services.root.utils import ErrorMessage, parse_message
from services.storage import StorageService
from services.utils import ensure_root

PERCENTAGE_EXTRACTOR = re.compile(" ([0-9]+)%")
NEWLINE_EXTRACTOR = re.compile("[\r\n]+")


class SourceService:
    """Service to handle sources."""

    def __init__(self) -> None:
        """SourceService."""
        self.storage_service = StorageService()
        self.sources_folder = self.storage_service.sources_folder

    def get_sources(self) -> list[Source]:
        """Get list of current sources.

        Returns
        -------
            List[Source]: sources

        """
        sources: list[Source] = []
        for name in os.listdir(self.sources_folder):
            path = self.abspath(name)
            if Path(path).is_dir():
                with Path(f"{path}/metadata.json").open(encoding="utf-8") as file:
                    source = Source.model_validate_json(file.read())
                sources.append(source)
        return sources

    def delete(self, name: str) -> None:
        """Delete a source.

        Args:
        ----
            name (str): name of source

        """
        shutil.rmtree(self.abspath(name), ignore_errors=True)

    def exists(self, name: str) -> bool:
        """Check if a source image exists with this name.

        Args:
        ----
            name (str): source image

        Returns:
        -------
            bool: if source image name exists

        """
        return Path(f"{self.sources_folder}/{name}").exists()

    def abspath(self, name: str) -> str:
        """Return path of source image.

        Args:
        ----
            name (str): source image

        Returns:
        -------
            str: absolute path to source image

        """
        return Path(f"{self.sources_folder}/{name}").resolve()


class DeviceSectorService:
    """Find sector size of last plugged drive."""

    def __init__(self, callback: Callable[[int], None]) -> None:
        """Build DeviceSectorService.

        Args:
        ----
            callback (Callable[[int], None]): called when a drive has been plugged.

        """
        self.context = pyudev.Context()
        self.callback = callback

        monitor = pyudev.Monitor.from_netlink(self.context)
        monitor.filter_by(subsystem="scsi", device_type="scsi_device")
        self.device_observer = pyudev.MonitorObserver(
            monitor,
            self._handle_monitor_event,
        )

        self.device_observer.start()

    def _handle_monitor_event(self, action: str, udev_device: pyudev.Device) -> None:
        """Receive a device event.

        Args:
        ----
            action (str): action
            udev_device (pyudev.Device): device

        """
        if action != "bind":
            return

        # sda, sdb, ...
        block_id = DeviceSectorService._find_block_id(udev_device.sys_path)

        sector_size_path = f"/sys/block/{block_id}/queue/hw_sector_size"
        if Path(sector_size_path).is_file():
            with Path(sector_size_path).open(encoding="utf-8") as f:
                try:
                    sector_size = int(f.read())
                    self.callback(sector_size)
                except ValueError:
                    pass

    @classmethod
    def _find_block_id(cls, sys_name: str) -> str:
        block_folder = f"{sys_name}/block"

        if Path(block_folder).is_dir():
            subdirectories = os.listdir(block_folder)
            if len(subdirectories) == 1:
                return subdirectories[0]
        return ""


class ComputeFat32SourceSizeWorker:
    """Compute source size."""

    def __init__(
        self,
        source_path: str,
        cluster_size: int,
        sector_size: int,
        num_fat_tables: int,
        callback: Callable[[int], None],
    ) -> None:
        """Build ComputeFat32SourceSizeWorker.

        Args:
        ----
            source_path (str): absolute path to source
            cluster_size (int): cluster size in byte
            sector_size (int): sector size in byte
            num_fat_tables (int): number of fat tables (usually 2)
            callback (Callable[[int], None]): callback to call after compute

        """
        super().__init__()
        self.source_path = source_path
        self.cluster_size = cluster_size
        self.sector_size = sector_size
        self.callback = callback
        self.num_fat_tables = num_fat_tables

    async def compute_size_file(self, file_path: str) -> int:
        """Compute size of file.

        Args:
        ----
            file_path (str): absolute path to file

        Returns:
        -------
            int: size in block of block_size

        """
        return math.ceil(Path(file_path).stat().st_size / self.cluster_size)

    async def compute_size_directory(self, directory_path: str) -> int:
        """Compute size of directory.

        Args:
        ----
            directory_path (str): absolute path to directory

        Returns:
        -------
            int: size in block of block_size

        """
        total_size = 0
        num_files = 0
        for file in os.listdir(directory_path):
            num_files += 1 + math.ceil(max(len(file) - 6, 0) / 13)
            file_path = Path(directory_path) / file
            total_size += await self.compute_size(file_path)

        total_size += math.ceil((1 + num_files) * 32 / self.cluster_size)
        return total_size

    async def compute_size(self, path: str) -> int:
        """Compute size of file or directory.

        Args:
        ----
            path (str): absolute path to file or directory

        Returns:
        -------
            int: size in block of block_size

        """
        if Path(path).is_dir():
            return await self.compute_size_directory(path)
        if Path(path).is_file():
            return await self.compute_size_file(path)

        return 0

    async def run(self) -> None:
        """Run task."""
        # Compute data region clusters
        data_region_clusters = await self.compute_size(self.source_path)

        # Compute fat table size
        fat_entries_per_cluster = self.cluster_size / 4
        fat_region_clusters = math.ceil(
            (data_region_clusters + 2) / fat_entries_per_cluster,
        )

        # Total size (in clusters)
        sectors_per_cluster = int(self.cluster_size / self.sector_size)
        total_clusters = (
            data_region_clusters
            + self.num_fat_tables * fat_region_clusters
            + math.ceil((32 + 1) / sectors_per_cluster)
        )
        total_clusters = math.ceil(total_clusters / 32) * 32

        # Convert to MB (+ alignment)
        total_size = 1 + math.ceil(total_clusters * self.cluster_size / (1024 * 1024))

        self.callback(total_size)


class CreateSourceImageWorker:
    """Service to create source image."""

    def __init__(
        self,
        source_path: str,
        cluster_size: int,
        sector_size: int,
        total_size: int,
        source_image_path: str,
        source_image_name: str,
        progress_callback: Callable[[int], None],
        callback: Callable[[str | None], None],
    ) -> None:
        """Build CreateSourceImageWorker.

        Args:
        ----
            source_path (str): path of folder containing source
            cluster_size (int): cluster size
            sector_size (int): sector size
            total_size (int): size of source image (in MB)
            source_image_path (str): output path of source image
            source_image_name (str): source image name
            progress_callback (Callable[[int], None]): called periodically to send
                information about source creation process
            callback (Callable[[Optional[str]], None]): called when source creation is
                finished

        """
        super().__init__()
        self.source_path = source_path
        self.source_image_path = source_image_path
        self.source_image_name = source_image_name
        self.sector_size = sector_size
        self.cluster_size = cluster_size
        self.total_size = total_size
        self.callback = callback
        self.progress_callback = progress_callback
        self.storage_service = StorageService()

    async def run(self) -> None:
        """Run source creation."""
        # Create source image
        proc = await asyncio.create_subprocess_exec(
            *ensure_root(
                [
                    str(sys.executable),
                    self.storage_service.src_folder / "services/root/create_source.py",
                    f"--source-path={self.source_path}",
                    f"--source-name={self.source_image_name}",
                    f"--source-size={self.total_size}",
                    f"--output-path={self.source_image_path}",
                    f"--cluster-size={self.cluster_size}",
                    f"--sector-size={self.sector_size}",
                    f"--uid={os.geteuid()}",
                ],
                cwd=str(self.storage_service.src_folder),
            ),
            stdout=asyncio.subprocess.PIPE,
        )

        error_message: ErrorMessage = None
        while (line := await proc.stdout.readline()) != b"":
            try:
                message = parse_message(line)
                match message.type:
                    case "progress":
                        self.progress_callback(message.value)
                    case "error":
                        error_message = message
            except ValueError:  # noqa: PERF203
                pass
        await proc.communicate()

        if proc.returncode != 0:
            shutil.rmtree(self.source_image_path, ignore_errors=True)

            if error_message is not None:
                self.callback(_(error_message.message))
            else:
                self.callback(_("Unknown error."))
        else:
            self.callback()
