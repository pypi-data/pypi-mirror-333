"""Services for USB management.

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
import contextlib
import os
import re
import subprocess
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING

import pyudev
from localization import _
from model.destination import Device
from services.root.utils import parse_message
from services.storage import StorageService
from services.utils import async_subprocess_check_output, ensure_root

if TYPE_CHECKING:
    from model.script import ErrorMessage

EXTRACT_DEVICE_NAME_REGEX = re.compile(
    r"^.*/usb[0-9]+/[^:]+/([0-9\-\.]+):[0-9\.]+/host.*$",
)
CLEAN_DEVICE_NAME_REGEX = re.compile(r"[\.\-]")


class UsbMonitorService:
    """Monitor connection disconnection of devices and disks."""

    def __init__(self, connection_callback: Callable[[Device], None]) -> None:
        """Build UsbMonitorService.

        Args:
        ----
            connection_callback (Callable[[Device], None]): called when a device is
                connected or disconnected

        """
        self.connection_callback = connection_callback
        self.context = pyudev.Context()

        monitor = pyudev.Monitor.from_netlink(self.context)
        monitor.filter_by(subsystem="scsi", device_type="scsi_device")
        self.device_observer = pyudev.MonitorObserver(
            monitor,
            self.handle_device_monitor_event,
        )

    def start(self) -> None:
        """Start monitoring devices."""
        self.device_observer.start()

    def stop(self) -> None:
        """Stop monitoring devices."""
        self.device_observer.stop()

    def enumerate_devices(self) -> list[Device]:
        """Enumerate devices currently connected.

        Returns
        -------
            List[Device]: list of devices currently connected

        """
        devices = []
        for udev_device in self.context.list_devices(
            subsystem="scsi",
            DEVTYPE="scsi_device",
        ):
            device_id = UsbMonitorService.compute_device_id(udev_device.sys_path)
            block_id = UsbMonitorService.find_block_id(udev_device.sys_path)
            device = Device(id=device_id, block_id=block_id, is_connected=True)
            devices.append(device)
        return devices

    def handle_device_monitor_event(
        self,
        action: str,
        udev_device: pyudev.Device,
    ) -> None:
        """Receive a device event.

        Args:
        ----
            action (str): action
            udev_device (pyudev.Device): device

        """
        is_connected = None
        match action:
            case "unbind":
                is_connected = False
            case "bind":
                is_connected = True

        if is_connected is not None:
            device_id = UsbMonitorService.compute_device_id(udev_device.sys_path)
            device = Device(id=device_id, is_connected=is_connected)

            if is_connected:
                block_id = UsbMonitorService.find_block_id(udev_device.sys_path)
                device.block_id = block_id

            self.connection_callback(device)

    @classmethod
    def compute_device_id(cls, sys_name: str) -> str:
        """Compute normalized device id (e.g., 3.2.3).

        Args:
        ----
            sys_name (str): sys name

        Returns:
        -------
            str: normalized device id

        """
        match = EXTRACT_DEVICE_NAME_REGEX.fullmatch(sys_name)
        raw_device_name = match.group(1)

        return CLEAN_DEVICE_NAME_REGEX.sub(".", raw_device_name)

    @classmethod
    def find_block_id(cls, sys_name: str) -> str:
        """Return block id associated to disk.

        Args:
        ----
            sys_name (str): sys name of disk

        Returns:
        -------
            str: block id (e.g., sda, sdb, ...)

        """
        block_folder = f"{sys_name}/block"
        if Path(block_folder).is_dir():
            subdirectories = os.listdir(block_folder)
            if len(subdirectories) == 1:
                return subdirectories[0]
        return None


class UsbSizeService:
    """Service to determine size of USB device."""

    def compute_total_space(self, block_id: str) -> int:
        """Compute block total space.

        Args:
        ----
            block_id (str): block id (e.g., sda, sdb, ...)

        Returns:
        -------
            int: total size in Bytes

        """
        with contextlib.suppress(Exception):
            output = subprocess.check_output(
                ["/usr/bin/lsblk", "-bno", "SIZE", f"/dev/{block_id}"],
            ).decode(encoding="utf-8")
            return int(output.splitlines()[0])
        return 0

    async def async_compute_total_space(self, block_id: str) -> int:
        """Compute total space.

        Args:
        ----
            block_id (str): block id (e.g., sda, sdb, ...)

        Returns:
        -------
            str: total size in Bytes

        """
        with contextlib.suppress(Exception):
            output = (
                await async_subprocess_check_output(
                    "/usr/bin/lsblk",
                    "-bno",
                    "SIZE",
                    f"/dev/{block_id}",
                )
            ).decode(encoding="utf-8")
            return int(output.splitlines()[0])
        return 0

    def compute_occupied_space(self, block_id: str) -> int:
        """Compute occupied space of block_id.

        Args:
        ----
            block_id (str): block

        Returns:
        -------
            int: occupied size in Bytes

        """
        device_path = f"/dev/{block_id}"

        # List partitions of destination
        partitions = []
        for partition in os.listdir("/dev"):
            partition_path = f"/dev/{partition}"
            if (
                partition_path != device_path
                and partition_path.startswith(device_path)
                and str.isdigit(partition_path[len(device_path) :])
            ):
                partitions.append(partition_path)

        # Mount each partition to get its occupied space
        occupied_space = 0
        with tempfile.TemporaryDirectory() as tmp_directory:
            for partition in partitions:
                with contextlib.suppress(Exception):
                    subprocess.check_call(["/usr/bin/mount", partition, tmp_directory])
                    output = subprocess.check_output(
                        ["/usr/bin/df", "--block-size=1M", "--output=used", partition],
                    )
                    occupied_space += int(output.split()[1])
                subprocess.run(["/usr/bin/umount", partition], check=False)

        return occupied_space * 1024 * 1024


class ComputeOccupiedSpaceWorker:
    """Worker to compute occupied space."""

    def __init__(
        self,
        devices: list[Device],
        progress_callback: Callable[[float], None],
        end_device_callback: Callable[[Device, int], None],
        end_callback: Callable[[str], None],
    ) -> None:
        """Build ComputeOccupiedSpaceWorker.

        Args:
        ----
            devices (List[Device]): devices
            progress_callback (Callable[[float], None]): called periodically to send
                process progress
            end_device_callback (Callable[[Device, int], None]): called when computation
                is finished for a device
            end_callback (Callable[[str], None]): called when process if finished.

        """
        self.devices = devices
        self.progress_callback = progress_callback
        self.end_callback = end_callback
        self.end_device_callback = end_device_callback

        self.storage_service = StorageService()

    async def run(self) -> None:
        """Run occupied space task."""
        proc = await asyncio.create_subprocess_exec(
            *ensure_root(
                [
                    sys.executable,
                    self.storage_service.src_folder
                    / "services/root/compute_occupied_space.py",
                    *[f"--block-id={device.block_id}" for device in self.devices],
                ],
                cwd=str(self.storage_service.src_folder),
            ),
            stdout=asyncio.subprocess.PIPE,
        )

        device_by_block_id = {device.block_id: device for device in self.devices}

        error_message: ErrorMessage = None
        while (line := await proc.stdout.readline()) != b"":
            try:
                message = parse_message(line)
                match message.type:
                    case "progress":
                        self.progress_callback(message.value)
                    case "error":
                        error_message = message
                    case "device_occupied_space":
                        self.end_device_callback(
                            device_by_block_id[message.block_id],
                            message.occupied_space,
                        )
            except ValueError:  # noqa: PERF203
                pass
        await proc.communicate()

        if proc.returncode != 0:
            if error_message is not None:
                self.end_callback(_(error_message.message))
            else:
                self.end_callback(_("Unknown error."))
        else:
            self.end_callback()
