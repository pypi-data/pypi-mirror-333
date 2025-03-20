"""Main view for hub management.

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
import pyperclip
from localization import _
from model.destination import Device, Hub
from services.destination import DestinationsService
from services.usb import UsbMonitorService
from view.hubs.creation import CreateHubDialog
from view.hubs.hub import HubView
from view.utils.banners import success_banner


class HubsView(ft.Container):
    """Main view for hub management."""

    def __init__(self) -> None:
        """Build HubsView."""
        super().__init__(expand=True)

        # Model & Services
        self.destinations_service = DestinationsService()
        self.hubs = self.destinations_service.get_hubs()

        self.usb_monitor_service = UsbMonitorService(self.on_event_device_connection)

        # View
        self.hub_tabs = ft.Tabs(
            animation_duration=300,
            selected_index=0,
            tabs=[HubView(hub, self.on_click_delete_hub) for hub in self.hubs],
            expand=True,
            expand_loose=True,
        )
        self.last_device_field = ft.TextField(
            value=_("none"),
            read_only=True,
            width=200,
        )
        self.last_device_button = ft.IconButton(
            icon=ft.icons.CONTENT_COPY,
            tooltip=_("Copy device address"),
            disabled=True,
            on_click=self.on_click_copy_disk,
        )
        self.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            _("Your hubs"),
                            theme_style=ft.TextThemeStyle.TITLE_LARGE,
                        ),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    _("Add a hub"),
                                    icon=ft.icons.ADD,
                                    on_click=self.on_click_add_hub,
                                ),
                                ft.FilledButton(
                                    _("Save"),
                                    icon=ft.icons.SAVE,
                                    on_click=self.on_click_save,
                                ),
                            ],
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.Text(_("Address of the last connected device")),
                        self.last_device_field,
                        self.last_device_button,
                    ],
                ),
                self.hub_tabs,
            ],
        )

    def did_mount(self) -> None:
        """Initialize services after view is mounted."""
        self.usb_monitor_service.start()

    def will_unmount(self) -> None:
        """Stop services before view is destroyed."""
        self.usb_monitor_service.stop()

    def on_click_delete_hub(self, hub_view: HubView) -> None:
        """Handle when user wants to delete hub.

        Args:
        ----
            hub_view (HubView): hub to delete

        """
        hub = hub_view.hub
        self.hubs.remove(hub)

        self.hub_tabs.tabs.remove(hub_view)
        self.update()

    def on_click_save(self, _event: ft.ControlEvent) -> None:
        """Save hubs.

        Args:
        ----
            _event (ft.ControlEvent): unused

        """
        self.destinations_service.save_hubs(self.hubs)

        page = self.page

        def close_banner() -> None:
            page.banner.open = False
            page.update()

        page.banner = success_banner(_("The hubs have been saved."), close_banner)
        page.banner.open = True
        page.update()

    def on_click_add_hub(self, _event: ft.ControlEvent) -> None:
        """Handle when user click on button to add hub.

        Args:
        ----
            _event (ft.ControlEvent): unused

        """
        dialog = CreateHubDialog(self.on_create_hub)
        self.page.dialog = dialog
        self.page.open(self.page.dialog)

    def on_create_hub(self, num_rows: int, num_columns: int) -> None:
        """Handle when user has validated modal.

        Args:
        ----
            num_rows (int): number of rows of hub
            num_columns (int): number of columns of hub

        """
        hub = Hub(
            num_columns=num_columns,
            num_rows=num_rows,
            ports=[""] * (num_rows * num_columns),
        )
        self.hubs.append(hub)
        self.hub_tabs.tabs.append(HubView(hub, self.on_click_delete_hub))
        self.update()

    def on_event_device_connection(self, device: Device) -> None:
        """Handle when a device is connected/disconnected.

        Args:
        ----
            device (Device): device

        """
        self.last_device_field.value = device.id
        self.last_device_button.disabled = False
        self.update()

    def on_click_copy_disk(self, _event: ft.ControlEvent) -> None:
        """Handle when user copy disk address.

        Args:
        ----
            _event (ft.ControlEvent): unused

        """
        pyperclip.copy(self.last_device_field.value)
