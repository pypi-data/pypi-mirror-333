"""Main view for copy.

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

import flet as ft
from babel.dates import format_datetime
from babel.numbers import format_number
from babel.units import get_unit_name
from localization import _, __byte_unit_length__, __locale__
from model.destination import Device, Hub
from model.source import Source
from services.copy import CopyPartitionWorker
from services.destination import DestinationsService
from services.settings import SettingsService
from services.source import SourceService
from services.usb import (
    ComputeOccupiedSpaceWorker,
    UsbMonitorService,
    UsbSizeService,
)
from view.copy.device import DeviceView
from view.utils.banners import error_banner, success_banner
from view.utils.progress import TimerProgressBar


class CopyView(ft.Container):
    """Main view for copy."""

    def __init__(self) -> None:
        """Build CopyView."""
        super().__init__(expand=True)

        # Model & Services
        self.destinations_service = DestinationsService()
        self.hubs = self.destinations_service.get_hubs()

        self.source_service = SourceService()
        self.sources = self.source_service.get_sources()
        self.source_index = -1
        if len(self.sources) > 0:
            self.source_index = 0

        self.devices: dict[str, DeviceView] = {}

        self.usb_monitor_service = UsbMonitorService(self.on_usb_monitor_event)
        self.usb_size_service = UsbSizeService()

        self.settings_service = SettingsService()
        self.settings = self.settings_service.load()

        # States: idle, copying, computing_occupied_space
        self.state = "idle"

        # View
        self.copy_button = ft.FilledButton(
            icon=ft.icons.PLAY_ARROW,
            text=_("Start copy"),
            on_click=self.on_click_start_copy,
        )
        self.occupied_space_button = ft.ElevatedButton(
            icon=ft.icons.SIGNAL_WIFI_STATUSBAR_4_BAR,
            text=_("Compute occupied space"),
            tooltip=_(
                "Compute the occupied space for each destination currently connected.",
            ),
            on_click=self.on_click_compute_occupied_space,
        )

        self.progress = TimerProgressBar(visible=False)
        self.content = ft.Column(
            [
                ft.Text(_("Source"), style=ft.TextThemeStyle.TITLE_LARGE),
                ft.Dropdown(
                    options=[
                        ft.dropdown.Option(
                            key=str(i),
                            text="{name} {creation_date} ({size} {unit})".format(
                                name=source.name,
                                creation_date=format_datetime(
                                    source.creation_date,
                                    locale=__locale__,
                                    format="short",
                                ),
                                size=format_number(source.size, locale=__locale__),
                                unit=get_unit_name(
                                    "digital-megabyte",
                                    locale=__locale__,
                                    length=__byte_unit_length__,
                                ),
                            ),
                        )
                        for i, source in enumerate(self.sources)
                    ],
                    value=str(self.source_index),
                    on_change=self.on_dropdown_source,
                ),
                ft.Text("Destinations", style=ft.TextThemeStyle.TITLE_LARGE),
                ft.Column([self.display_hub(hub) for hub in self.hubs]),
                ft.Row([self.occupied_space_button, self.copy_button]),
                self.progress,
            ],
            scroll=ft.ScrollMode.AUTO,
        )

    def did_mount(self) -> None:
        """Initialize services after view is mounted."""
        # Initialize devices
        connected_devices = self.usb_monitor_service.enumerate_devices()
        for device in connected_devices:
            if device.id in self.devices:
                self.devices[device.id].set_device(device)
                self.page.run_task(self.compute_total_space, device)
        self.usb_monitor_service.start()

    def will_unmount(self) -> None:
        """Stop services before view is destroyed."""
        self.usb_monitor_service.stop()

    def change_state(self, new_state: str) -> None:
        """Change application state.

        Args:
        ----
            new_state (str): state

        """
        match self.state:
            case "copying":
                self.progress.visible = False
                self.progress.value = None
                self.enable_copy(enabled=True)
                self.enable_occupied(enabled=True)
                self.page.enable_rail(enabled=True)
                self.page.confirm_exit = None
                self.update()
            case "computing_occupied_space":
                self.progress.visible = False
                self.progress.value = None
                self.enable_copy(enabled=True)
                self.enable_occupied(enabled=True)
                self.page.enable_rail(enabled=True)
                self.page.confirm_exit = None
                self.update()

        self.state = new_state

        match self.state:
            case "copying":
                self.progress.visible = True
                self.enable_copy(enabled=False)
                self.enable_occupied(enabled=False)
                self.page.enable_rail(enabled=False)
                self.page.confirm_exit = _("A copy is in progress.")
                self.update()
            case "computing_occupied_space":
                self.progress.visible = True
                self.enable_copy(enabled=False)
                self.enable_occupied(enabled=False)
                self.page.enable_rail(enabled=False)
                self.page.confirm_exit = _(
                    "Occupied space is currently being calculated.",
                )
                self.update()

    def display_hub(self, hub: Hub) -> ft.Control:
        """Display a hub.

        Args:
        ----
            hub (Hub): hub

        Returns:
        -------
            ft.Control: view to display

        """
        devices = [DeviceView(port_id) for port_id in hub.ports]
        for device in devices:
            self.devices[device.port_id] = device

        return ft.Row(
            [
                ft.Column(
                    [
                        ft.Row(
                            [
                                devices[i * hub.num_columns + j]
                                for j in range(hub.num_columns)
                            ],
                        )
                        for i in range(hub.num_rows)
                    ],
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        )

    def on_click_start_copy(self, _event: ft.ControlEvent) -> None:
        """When user click to start copy.

        Args:
        ----
            _event (ft.ControlEvent): unused

        """
        page = self.page

        def close_banner() -> None:
            page.banner.open = False
            page.update()

        # Check if there is a source
        source = None
        if self.source_index >= 0 and self.source_index < len(self.sources):
            source = self.sources[self.source_index]
        if source is None:
            page.banner = error_banner(
                _("Copy could not be started: no source selected."),
                close_banner,
            )
            page.banner.open = True
            page.update()
            return

        # Check if there are destinations
        destinations = []
        for view in self.devices.values():
            device = view.device
            if device is not None and device.is_connected:
                destinations.append(view.device)
        if len(destinations) == 0:
            page.banner = error_banner(
                _("No destination is currently connected."),
                close_banner,
            )
            page.banner.open = True
            page.update()
            return

        # Display confirmation
        def cancel_modal(_event: ft.ControlEvent) -> None:
            dialog.open = False
            self.page.update()

        def start_copy(_event: ft.ControlEvent) -> None:
            dialog.open = False
            self.page.update()
            self.on_validate_start_copy(source, destinations)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(_("Start copy")),
            content=ft.Text(
                _(
                    """You are about to launch a copy
Source: {source}
Destinations: {destinations}
            """,
                ).format(
                    source=source.name,
                    destinations=", ".join(
                        [destination.block_id for destination in destinations],
                    ),
                ),
            ),
            actions=[
                ft.TextButton(_("Cancel"), on_click=cancel_modal),
                ft.TextButton(_("Copy"), icon=ft.icons.PLAY_ARROW, on_click=start_copy),
            ],
        )
        self.page.dialog = dialog
        self.page.open(self.page.dialog)

    def on_click_compute_occupied_space(self, _event: ft.ControlEvent) -> None:
        """When user click to start computing occupied space."""
        page = self.page

        def close_banner() -> None:
            page.banner.open = False
            page.update()

        # Check if there are devices
        devices = []
        for view in self.devices.values():
            if view.device is not None and view.device.is_connected:
                (devices.append(view.device),)
        if len(devices) == 0:
            page.banner = error_banner(
                _("No destination is currently connected."),
                close_banner,
            )
            page.banner.open = True
            page.update()
            return

        # Launch task
        self.change_state("computing_occupied_space")
        self.progress.value = 0

        for device in devices:
            view = self.devices.get(device.id, None)
            if view is not None:
                view.set_state("occupied")

        worker = ComputeOccupiedSpaceWorker(
            devices,
            self.on_progress_change,
            self.on_device_occupied_finished,
            self.on_occupied_finished,
        )
        self.page.run_task(worker.run)

    def on_progress_change(self, value: float) -> None:
        """When progress has changed.

        Args:
        ----
            value (float): value

        """
        self.progress.value = value

    def on_device_copy_finished(
        self,
        device: Device,
        success: bool,  # noqa: FBT001
        occupied_space: int,
    ) -> None:
        """When copy is finished for a device.

        Args:
        ----
            device (Device): device
            success (bool): success
            occupied_space (int): occupied space

        """
        view = self.devices.get(device.id, None)
        if view is not None:
            view.set_state("success" if success else "error")
            view.set_occupied_space(occupied_space)

    def on_device_occupied_finished(self, device: Device, occupied_space: int) -> None:
        """When compute occupied space is finished for a device.

        Args:
        ----
            device (Device): device
            occupied_space (int): occupied space

        """
        view = self.devices.get(device.id, None)
        if view is not None:
            view.set_state("idle")
            view.set_occupied_space(occupied_space)

    def on_validate_start_copy(
        self,
        source: Source,
        destinations: list[Device],
    ) -> None:
        """When user has validated copy.

        Args:
        ----
            source (Source): source of copy
            destinations (List[Device]): destinations

        """
        self.change_state("copying")
        self.progress.value = 0

        for destination in destinations:
            view = self.devices.get(destination.id, None)
            if view is not None:
                view.set_state("occupied")

        worker = CopyPartitionWorker(
            source,
            destinations,
            self.settings.copy_num_destinations_per_process,
            self.on_progress_change,
            self.on_device_copy_finished,
            self.on_copy_finished,
        )
        self.page.run_task(worker.run)

    def on_copy_finished(self, error: str | None = None) -> None:
        """When copy is finished.

        Args:
        ----
            error (str): optional error

        """
        page = self.page
        self.change_state("idle")

        def close_banner() -> None:
            page.banner.open = False
            page.update()

        if error is not None:
            page.banner = error_banner(
                _("The copy failed.") + " " + error,
                close_banner,
            )
        else:
            page.banner = success_banner(_("Copy complete!"), close_banner)
        page.banner.open = True
        page.update()

    def on_occupied_finished(self, error: str | None = None) -> None:
        """When compute occupied is finished.

        Args:
        ----
            error (str): optional error

        """
        page = self.page
        self.change_state("idle")

        def close_banner() -> None:
            page.banner.open = False
            page.update()

        if error is not None:
            page.banner = error_banner(
                _("Occupied space computation failed.") + " " + error,
                close_banner,
            )
        else:
            page.banner = success_banner(_("Computation complete!"), close_banner)
        page.banner.open = True
        page.update()

    def on_dropdown_source(self, event: ft.ControlEvent) -> None:
        """When use changes source.

        Args:
        ----
            event (ft.ControlEvent): event

        """
        source_index = event.data
        if source_index.isdigit():
            self.source_index = int(source_index)

    async def compute_total_space(self, device: Device) -> None:
        """Compute device total space.

        Args:
        ----
            device (Device): device

        """
        total_space = await self.usb_size_service.async_compute_total_space(
            device.block_id,
        )
        if device.id in self.devices:
            self.devices[device.id].set_total_space(total_space)

    def on_usb_monitor_event(self, device: Device) -> None:
        """When usb monitor events.

        Args:
        ----
            device (Device): device

        """
        if device.id in self.devices:
            view = self.devices[device.id]
            found_device = view.device

            if found_device is not None:
                view.set_is_connected(device.is_connected)
                view.set_block_id(device.block_id)
            else:
                view.set_device(device)

            if device.is_connected:
                self.page.run_task(self.compute_total_space, device)

    def enable_copy(self, *, enabled: bool) -> None:
        """Enable/Disable copy.

        Args:
        ----
            enabled (bool): enabled

        """
        self.copy_button.disabled = not enabled
        self.update()

    def enable_occupied(self, *, enabled: bool) -> None:
        """Enable/Disable occupied space compute.

        Args:
        ----
            enabled (bool): enabled

        """
        self.occupied_space_button.disabled = not enabled
        self.update()
