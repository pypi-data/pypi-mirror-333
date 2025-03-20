"""View to display and modify a hub.

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

import functools
from collections.abc import Callable

import flet as ft
from localization import _
from model.destination import Hub


class PortView(ft.TextField):
    """View to display and modify port."""

    def __init__(self, address: str, change_callback: Callable[[str], None]) -> None:
        """Build PortView.

        Args:
        ----
            address (str): new initial port address
            change_callback (Callable[[int, str], None]): called when address is changed

        """
        super().__init__(
            value=address,
            on_change=lambda _: change_callback(self.value),
            width=150,
            label=_("Address"),
        )


class HubView(ft.Tab):
    """Hub view."""

    def __init__(self, hub: Hub, on_delete: Callable[["HubView"], None]) -> None:
        """Build HubView.

        Args:
        ----
            hub (Hub): hub
            on_delete (Callable[[HubView], None]): called when user wants to delete hub

        """
        super().__init__(text=_("Hub"))
        self.hub = hub
        self.on_delete_callback = on_delete

        self.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            _("{num_rows} rows x {num_columns} columns").format(
                                num_rows=self.hub.num_rows,
                                num_columns=self.hub.num_columns,
                            ),
                        ),
                        ft.ElevatedButton(
                            _("Delete this hub"),
                            icon=ft.icons.DELETE,
                            on_click=self.on_click_delete,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Row(
                                    [
                                        PortView(
                                            self.hub.ports[
                                                i * self.hub.num_columns + j
                                            ],
                                            functools.partialmethod(
                                                self.on_port_change,
                                                i * self.hub.num_columns + j,
                                            ),
                                        )
                                        for j in range(self.hub.num_columns)
                                    ],
                                )
                                for i in range(self.hub.num_rows)
                            ],
                        ),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        )

    def on_click_delete(self, _event: ft.ControlEvent) -> None:
        """Handle when user click on delete button.

        Args:
        ----
            _event (ft.ControlEvent): unused

        """

        def cancel_modal(_event: ft.ControlEvent) -> None:
            dialog.open = False
            self.page.update()

        def confirm_delete(_event: ft.ControlEvent) -> None:
            dialog.open = False
            self.page.update()
            self.on_delete_callback(self)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(_("Hub deletion")),
            content=ft.Text(_("Do you want to delete the hub?")),
            actions=[
                ft.TextButton(_("Cancel"), on_click=cancel_modal),
                ft.TextButton(_("Delete permanently"), on_click=confirm_delete),
            ],
        )
        self.page.dialog = dialog
        self.page.open(self.page.dialog)

    def on_port_change(self, index: int, value: str) -> None:
        """Handle update port.

        Args:
        ----
            index (int): index of port
            value (str): value of port

        """
        self.hub.ports[index] = value
