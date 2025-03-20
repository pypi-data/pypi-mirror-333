"""Display sources.

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

import subprocess
from collections.abc import Callable

import flet as ft
from babel.dates import format_datetime
from babel.numbers import format_number
from babel.units import get_unit_name
from localization import _, __byte_unit_length__, __locale__
from services.source import Source, SourceService


class SourceView(ft.DataRow):
    """Display sources."""

    def __init__(
        self,
        source: Source,
        on_delete: Callable[["SourceView"], None],
    ) -> None:
        """Build SourceView.

        Args:
        ----
            source (Source): source
            on_delete (Callable[[SourceView], None]): called when user wants to delete
                source

        """
        super().__init__(cells=[])
        self.source = source
        self.on_delete_callback = on_delete

        self.cells.extend(
            [
                ft.DataCell(ft.Text(self.source.name)),
                ft.DataCell(
                    ft.Text(format_number(self.source.size, locale=__locale__)),
                ),
                ft.DataCell(
                    ft.Text(format_number(self.source.cluster_size, locale=__locale__)),
                ),
                ft.DataCell(
                    ft.Text(format_number(self.source.sector_size, locale=__locale__)),
                ),
                ft.DataCell(
                    ft.Text(
                        format_datetime(self.source.creation_date, locale=__locale__),
                    ),
                ),
                ft.DataCell(
                    ft.IconButton(
                        ft.icons.DELETE,
                        tooltip=_("Delete source"),
                        on_click=self.on_click_delete,
                    ),
                ),
            ],
        )

    def on_click_delete(self, _event: ft.ControlEvent) -> None:
        """When user click to delete source.

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
            title=ft.Text(
                _('Delete source "{source}"').format(
                    source=self.source.name,
                ),
            ),
            content=ft.Text(
                _('Do you want to delete the source "{source}" ?').format(
                    source=self.source.name,
                ),
            ),
            actions=[
                ft.TextButton(_("Cancel"), on_click=cancel_modal),
                ft.TextButton(_("Delete permanently"), on_click=confirm_delete),
            ],
        )
        self.page.dialog = dialog
        self.page.open(self.page.dialog)


class SourceListView(ft.Column):
    """Display and manage the list of sources."""

    def __init__(self) -> None:
        """Build SourceListView."""
        super().__init__(alignment=ft.MainAxisAlignment.START)

        # Model & Services
        self.source_service = SourceService()
        self.sources = self.source_service.get_sources()

        # View
        self.sources_view = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text(_("Name"))),
                ft.DataColumn(
                    ft.Text(
                        _("Size")
                        + " ({unit})".format(
                            unit=get_unit_name(
                                "digital-megabyte",
                                locale=__locale__,
                                length=__byte_unit_length__,
                            ),
                        ),
                    ),
                    numeric=True,
                ),
                ft.DataColumn(
                    ft.Text(
                        _("Block size")
                        + " ({unit})".format(
                            unit=get_unit_name(
                                "digital-byte",
                                locale=__locale__,
                                length=__byte_unit_length__,
                            ),
                        ),
                    ),
                    numeric=True,
                ),
                ft.DataColumn(
                    ft.Text(
                        _("Cluster size")
                        + " ({unit})".format(
                            unit=get_unit_name(
                                "digital-byte",
                                locale=__locale__,
                                length=__byte_unit_length__,
                            ),
                        ),
                    ),
                    numeric=True,
                ),
                ft.DataColumn(ft.Text(_("Creation date"))),
                ft.DataColumn(ft.Text()),
            ],
            rows=[
                SourceView(source, self.on_click_delete_source)
                for source in self.sources
            ],
        )
        self.controls.extend(
            [
                ft.Row(
                    [
                        ft.Text(_("Folder where your sources are stored")),
                        ft.IconButton(
                            ft.icons.DRIVE_FOLDER_UPLOAD,
                            tooltip=_("Open the folder"),
                            on_click=self.on_click_open_sources_folder,
                        ),
                    ],
                ),
                ft.Row([self.sources_view], scroll=ft.ScrollMode.AUTO),
            ],
        )

    def on_click_delete_source(self, source_view: SourceView) -> None:
        """Handle delete source.

        Args:
        ----
            source_view (SourceView): source

        """
        source = source_view.source
        self.source_service.delete(source.name)
        self.sources.remove(source)
        self.sources_view.rows.remove(source_view)
        self.update()

    def on_click_open_sources_folder(self, _event: ft.ControlEvent) -> None:
        """Handle click event to open source folder.

        Args:
        ----
            _event (ft.ControlEvent): unused

        """
        subprocess.Popen(["/usr/bin/xdg-open", self.source_service.sources_folder])
