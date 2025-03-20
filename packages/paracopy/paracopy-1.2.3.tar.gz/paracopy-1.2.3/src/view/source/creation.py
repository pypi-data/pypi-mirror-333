"""View to create source.

Copyright (c) 2024 - 2025 Pierre-Yves Genest.

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
from babel.numbers import format_number
from babel.units import get_unit_name
from pathvalidate import ValidationError, validate_filename

from localization import _, __byte_unit_length__, __locale__
from services.source import (
    ComputeFat32SourceSizeWorker,
    CreateSourceImageWorker,
    DeviceSectorService,
    SourceService,
)
from view.utils.banners import error_banner, success_banner
from view.utils.progress import TimerProgressBar


class SourceCreationView(ft.Column):
    """View to create source."""

    def __init__(self) -> None:
        """Build SourceCreationView."""
        super().__init__(alignment=ft.MainAxisAlignment.START)

        # Model
        self.source_path: str = None
        self.cluster_size: int = 4096
        self.sector_size: int = 512
        self.last_sector_size: int = -1
        self.source_image_name: str = ""
        self.source_size: int = 0  # Source size in MB
        self.additional_mb: int = 0  # Additional MB to add to source

        # States: "idle", "source_chosen", "computing_size", "size_computed",
        # "copying"
        self.state: str = "idle"

        # Services
        self.source_service = SourceService()
        self.device_sector_size_service = DeviceSectorService(self.set_last_sector_size)

        # View
        self.pick_source_path_dialog = None
        self.source_image_name_field = ft.TextField(
            label=_("Source Name"),
            on_change=self.on_change_source_image_name,
        )

        self.choose_source_path_button = ft.IconButton(
            icon=ft.icons.FOLDER_SHARP,
            tooltip=_("Choose the source folder"),
            on_click=self.on_click_choose_source,
        )
        self.source_path_field = ft.TextField(
            label=_("Source folder for source image"),
            read_only=True,
        )
        self.last_sector_size_text = ft.Text(_("none"))

        self.compute_size_button = ft.ElevatedButton(
            text=_("Compute the size of the source"),
            icon=ft.icons.DATA_USAGE,
            on_click=self.on_start_computing_size,
        )
        self.source_size_text = ft.Text("0")
        self.additional_mb_field = ft.TextField(
            value="0",
            on_change=self.on_change_additional_mb,
            width=200,
        )
        self.total_size_text = ft.Text("0")

        self.create_source_button = ft.ElevatedButton(
            text=_("Create source"),
            icon=ft.icons.CREATE,
            on_click=self.on_start_creating_source,
        )

        self.progress_bar = TimerProgressBar(visible=False)

        self.controls.extend(
            [
                ft.Row([self.source_image_name_field]),
                ft.Row(
                    [
                        self.source_path_field,
                        self.choose_source_path_button,
                        ft.IconButton(
                            icon=ft.icons.INFO,
                            icon_color="black",
                            tooltip=_(
                                "Folders inside the selected folder "
                                "will be copied. The name of the selected folder "
                                "will not be copied."
                                "Warning: Folders and file names must not contain "
                                "accents or special characters!",
                            ),
                        ),
                    ],
                ),
                ft.Row(
                    [
                        ft.Dropdown(
                            label=_("Choose cluster size"),
                            options=[
                                ft.dropdown.Option(
                                    key="2048",
                                    text=format_number(2048, locale=__locale__)
                                    + " (2 {unit})".format(
                                        unit=get_unit_name(
                                            "digital-kilobyte",
                                            locale=__locale__,
                                            length=__byte_unit_length__,
                                        ),
                                    ),
                                ),
                                ft.dropdown.Option(
                                    key="4096",
                                    text=format_number(4096, locale=__locale__)
                                    + " (4 {unit})".format(
                                        unit=get_unit_name(
                                            "digital-kilobyte",
                                            locale=__locale__,
                                            length=__byte_unit_length__,
                                        ),
                                    ),
                                ),
                                ft.dropdown.Option(
                                    key="8192",
                                    text=format_number(8192, locale=__locale__)
                                    + " (16 {unit})".format(
                                        unit=get_unit_name(
                                            "digital-kilobyte",
                                            locale=__locale__,
                                            length=__byte_unit_length__,
                                        ),
                                    ),
                                ),
                                ft.dropdown.Option(
                                    key="16384",
                                    text=format_number(16384, locale=__locale__)
                                    + " (16 {unit})".format(
                                        unit=get_unit_name(
                                            "digital-kilobyte",
                                            locale=__locale__,
                                            length=__byte_unit_length__,
                                        ),
                                    ),
                                ),
                            ],
                            value=str(self.cluster_size),
                            on_change=self.on_dropdown_cluster_size,
                            width=200,
                        ),
                        ft.IconButton(
                            icon=ft.icons.INFO,
                            icon_color="black",
                            tooltip=_(
                                "As a rule of thumb:\n"
                                "- 2 {kb} = source size < 512 {mb}\n"
                                "- 4 {kb} = 512 {mb} – 8 {gb}\n"
                                "- 8 {kb} = 8 – 16 {gb}\n"
                                "- 16 {kb} = 16 – 32 {gb}",
                            ).format(
                                gb=get_unit_name(
                                    "digital-gigabyte",
                                    locale=__locale__,
                                    length=__byte_unit_length__,
                                ),
                                mb=get_unit_name(
                                    "digital-megabyte",
                                    locale=__locale__,
                                    length=__byte_unit_length__,
                                ),
                                kb=get_unit_name(
                                    "digital-kilobyte",
                                    locale=__locale__,
                                    length=__byte_unit_length__,
                                ),
                            ),
                        ),
                    ],
                ),
                ft.Row(
                    [
                        ft.Dropdown(
                            label=_("Choose sector size"),
                            options=[
                                ft.dropdown.Option(
                                    key="512",
                                    text=format_number(512, locale=__locale__)
                                    + " (512 {unit})".format(
                                        unit=get_unit_name(
                                            "digital-byte",
                                            locale=__locale__,
                                            length=__byte_unit_length__,
                                        ),
                                    ),
                                ),
                                ft.dropdown.Option(
                                    key="4096",
                                    text=format_number(4096, locale=__locale__)
                                    + " (4 {unit})".format(
                                        unit=get_unit_name(
                                            "digital-kilobyte",
                                            locale=__locale__,
                                            length=__byte_unit_length__,
                                        ),
                                    ),
                                ),
                            ],
                            value=str(self.sector_size),
                            on_change=self.on_dropdown_sector_size,
                            width=200,
                        ),
                        ft.IconButton(
                            icon=ft.icons.INFO,
                            icon_color="black",
                            tooltip=_(
                                "Check sector size for SD card or target USB disk. "
                                "A good default value is 512 {B}.",
                            ).format(
                                B=get_unit_name(
                                    "digital-byte",
                                    locale=__locale__,
                                    length=__byte_unit_length__,
                                ),
                            ),
                        ),
                        ft.Text(_("Sector size of the last plugged disk")),
                        self.last_sector_size_text,
                    ],
                    wrap=True,
                ),
                self.compute_size_button,
                ft.Row(
                    [
                        ft.Text(_("Source size:")),
                        self.source_size_text,
                        ft.Text("+"),
                        self.additional_mb_field,
                        ft.Text(
                            get_unit_name(
                                "digital-megabyte",
                                locale=__locale__,
                                length=__byte_unit_length__,
                            )
                            + " = ",
                        ),
                        self.total_size_text,
                        ft.Text(
                            get_unit_name(
                                "digital-megabyte",
                                locale=__locale__,
                                length=__byte_unit_length__,
                            ),
                        ),
                    ],
                    wrap=True,
                ),
                ft.Row([self.create_source_button]),
                self.progress_bar,
            ],
        )

    def did_mount(self) -> None:
        """Initialize services after view creation."""
        self.change_state("idle")

    def change_state(self, new_state: str) -> None:
        """Change state.

        Args:
        ----
            new_state (str): new state

        """
        # Close previous state
        match self.state:
            case "computing_size":
                self.page.enable_rail(enabled=True)
                self.page.confirm_exit = None
                self.progress_bar.visible = False
                self.progress_bar.value = None
                self.update()
            case "copying":
                self.page.enable_rail(enabled=True)
                self.page.confirm_exit = None
                self.progress_bar.visible = False
                self.progress_bar.value = None
                self.update()
            case _:
                pass

        self.state = new_state

        # Initialize new state
        match self.state:
            case "idle":
                self.enable_choose_source_path(enabled=True)
                self.enable_create_source_image(enabled=False)
                self.enable_compute_size(enabled=False)
            case "source_chosen":
                self.enable_compute_size(enabled=True)
                self.enable_create_source_image(enabled=False)
            case "computing_size":
                self.page.enable_rail(enabled=False)
                self.page.confirm_exit = _("Source size computation is in progress.")
                self.enable_choose_source_path(enabled=False)
                self.enable_create_source_image(enabled=False)
                self.enable_compute_size(enabled=False)
                self.progress_bar.visible = True
                self.progress_bar.value = None
                self.update()
            case "size_computed":
                self.enable_choose_source_path(enabled=True)
                self.enable_create_source_image(enabled=True)
                self.enable_compute_size(enabled=True)
            case "copying":
                self.page.enable_rail(enabled=False)
                self.page.confirm_exit = _("Source is currently being created.")
                self.enable_choose_source_path(enabled=False)
                self.enable_create_source_image(enabled=False)
                self.enable_compute_size(enabled=False)
                self.progress_bar.visible = True
                self.progress_bar.value = 0
                self.update()
            case _:
                pass

    def on_start_creating_source(self, _event: ft.ControlEvent) -> None:
        """Start creating source.

        Args:
        ----
            _event (ft.ControlEvent): event

        """
        # Check if source has correct name
        if self.source_image_name == "":
            self.source_image_name_field.error_text = _("Cannot be empty")
            self.update()
            return

        if self.source_service.exists(self.source_image_name):
            return

        self.change_state("copying")
        total_size = self.source_size + self.additional_mb
        source_image_path = self.source_service.abspath(self.source_image_name)
        worker = CreateSourceImageWorker(
            self.source_path,
            self.cluster_size,
            self.sector_size,
            total_size,
            source_image_path,
            self.source_image_name,
            self.set_progress,
            self.on_end_creating_source,
        )
        self.page.run_task(worker.run)

    def on_end_creating_source(self, error: str | None = None) -> None:
        """When copy is finished.

        Args:
        ----
            error (str): optional error

        """
        page = self.page
        self.change_state("size_computed")

        def close_banner() -> None:
            page.banner.open = False
            page.update()

        if error is not None:
            page.banner = error_banner(
                _("Source creation failed. ") + error,
                close_banner,
            )
        else:
            page.banner = success_banner(_("Source created!"), close_banner)
        page.banner.open = True
        page.update()

    def on_start_computing_size(self, _event: ft.ControlEvent) -> None:
        """Start computing size.

        Args:
        ----
            _event (ft.ControlEvent): event

        """
        self.change_state("computing_size")
        worker = ComputeFat32SourceSizeWorker(
            self.source_path,
            self.cluster_size,
            self.sector_size,
            2,
            self.on_end_computing_size,
        )
        self.page.run_task(worker.run)

    def on_end_computing_size(self, source_size: int) -> None:
        """When computing size has finished.

        Args:
        ----
            source_size (int): source size

        """
        self.change_state("size_computed")
        self.set_source_size(source_size)

    def on_change_additional_mb(self, event: ft.ControlEvent) -> None:
        """When additional mb value has changed.

        Args:
        ----
            event (ft.ControlEvent): event

        """
        additional_mb = event.data

        if str.isdigit(additional_mb) and int(additional_mb) >= 0:
            self.set_additional_mb(int(additional_mb))
            self.additional_mb_field.error_text = None
            self.update()
        else:
            self.set_additional_mb(0)
            self.additional_mb_field.error_text = _("Invalid size")
            self.update()

    def on_dropdown_cluster_size(self, event: ft.ControlEvent) -> None:
        """When cluster size has changed.

        Args:
        ----
            event (ft.ControlEvent): event

        """
        cluster_size = event.data
        if cluster_size is not None and str.isdigit(cluster_size):
            self.set_cluster_size(int(cluster_size))

    def on_dropdown_sector_size(self, event: ft.ControlEvent) -> None:
        """When sector size has changed.

        Args:
        ----
            event (ft.ControlEvent): event

        """
        sector_size = event.data
        if sector_size is not None and str.isdigit(sector_size):
            self.set_sector_size(int(sector_size))

    def on_click_choose_source(self, _event: ft.ControlEvent) -> None:
        """Choose source path."""
        if self.pick_source_path_dialog is None:

            def pick_source_path_result(event: ft.FilePickerResultEvent) -> None:
                source_path = event.path
                if source_path is not None:
                    self.set_source_path(source_path)
                    self.change_state("source_chosen")

            self.pick_source_path_dialog = ft.FilePicker(
                on_result=pick_source_path_result,
            )
            self.page.overlay.append(self.pick_source_path_dialog)
            self.page.update()

        self.pick_source_path_dialog.get_directory_path(
            dialog_title=_("Choose the folder for the source"),
        )

    def on_change_source_image_name(self, event: ft.ControlEvent) -> None:
        """When source image name has changed.

        Args:
        ----
            event (ft.ControlEvent): event

        """
        source_image_name = event.data
        error = False
        error_text = ""

        # Check source image name is a valid file name
        try:
            validate_filename(source_image_name)
        except ValidationError:
            error = True
            error_text = _("Invalid folder name")

        # Check if a source exists with this name
        if self.source_service.exists(source_image_name):
            error = True
            error_text = _("A source with the same name already exists")

        if error:
            self.source_image_name_field.error_text = error_text
            self.update()
            self.set_source_image_name("")
        else:
            self.source_image_name_field.error_text = None
            self.update()
            self.set_source_image_name(source_image_name)

    def enable_choose_source_path(self, *, enabled: bool) -> None:
        """Enable/Disable compute size button.

        Args:
        ----
            enabled (bool): enabled

        """
        self.choose_source_path_button.disabled = not enabled
        self.update()

    def enable_compute_size(self, *, enabled: bool) -> None:
        """Enable/Disable compute size button.

        Args:
        ----
            enabled (bool): enabled

        """
        self.compute_size_button.disabled = not enabled
        self.update()

    def enable_create_source_image(self, *, enabled: bool) -> None:
        """Enable/Disable create source button.

        Args:
        ----
            enabled (bool): enabled

        """
        self.create_source_button.disabled = not enabled
        self.update()

    def set_progress(self, progress: float) -> None:
        """Change progressbar progress.

        Args:
        ----
            progress (float): progress

        """
        self.progress_bar.value = progress
        self.update()

    def set_source_image_name(self, source_image_name: str) -> None:
        """Change source image name.

        Args:
        ----
            source_image_name (str): source image name

        """
        self.source_image_name = source_image_name

    def set_source_size(self, source_size: int) -> None:
        """Set source size.

        Args:
        ----
            source_size (int): source size

        """
        self.source_size = source_size
        self.source_size_text.value = self.source_size
        self.total_size_text.value = self.source_size + self.additional_mb
        self.update()

    def set_additional_mb(self, additional_mb: int) -> None:
        """Set additional mb.

        Args:
        ----
            additional_mb (int): additional mb

        """
        self.additional_mb = additional_mb
        self.total_size_text.value = self.source_size + self.additional_mb
        self.update()

    def set_source_path(self, source_path: str) -> None:
        """Set source path.

        Args:
        ----
            source_path (str): set source path

        """
        self.source_path = source_path
        self.source_path_field.value = source_path
        self.update()

    def set_cluster_size(self, cluster_size: int) -> None:
        """Set cluster size.

        Args:
        ----
            cluster_size (int): cluster size

        """
        self.cluster_size = cluster_size

    def set_sector_size(self, sector_size: int) -> None:
        """Set sector size.

        Args:
        ----
            sector_size (int): sector size

        """
        self.sector_size = sector_size

    def set_last_sector_size(self, sector_size: int) -> None:
        """Set sector size of last plugged device.

        Args:
        ----
            sector_size (int): sector size

        """
        self.last_sector_size = sector_size

        sector_size_text = ""
        match self.last_sector_size:
            case 512:
                sector_size_text = "512 {unit}".format(
                    unit=get_unit_name(
                        "digital-byte",
                        locale=__locale__,
                        length=__byte_unit_length__,
                    ),
                )
            case 4096:
                sector_size_text = "4 {unit}".format(
                    unit=get_unit_name(
                        "digital-megabyte",
                        locale=__locale__,
                        length=__byte_unit_length__,
                    ),
                )
            case _:
                sector_size_text = format_number(
                    self.last_sector_size,
                    locale=__locale__,
                    length=__byte_unit_length__,
                ) + " {unit}".format(
                    unit=get_unit_name(
                        "digital-byte",
                        locale=__locale__,
                        length=__byte_unit_length__,
                    ),
                )

        self.last_sector_size_text.value = sector_size_text
        self.update()
