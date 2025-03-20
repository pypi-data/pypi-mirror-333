"""Main view for settings.

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
from localization import _
from services.settings import SettingsService
from services.shortcut import ShortcutService
from view.utils.banners import success_banner


class SettingsView(ft.Container):
    """Main view for settings."""

    def __init__(self) -> None:
        """Construct SettingsView."""
        super().__init__(expand=True)

        # Model/Services
        self.settings_service = SettingsService()
        self.settings = self.settings_service.load()

        # View
        self.copy_num_destinations_per_process_field = ft.TextField(
            label=_("Number of destinations per copy process"),
            value=str(self.settings.copy_num_destinations_per_process),
            on_change=self.on_copy_num_destinations_per_process_change,
        )
        self.content = ft.Column(
            controls=[
                ft.Row(
                    [
                        ft.Text(
                            _("Settings"),
                            theme_style=ft.TextThemeStyle.TITLE_LARGE,
                            expand=True,
                        ),
                        ft.FilledButton(
                            icon=ft.icons.SAVE,
                            text=_("Save"),
                            on_click=self.on_click_save,
                        ),
                    ],
                ),
                ft.Text(
                    _("Installation settings"),
                    theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                ),
                ft.ElevatedButton(
                    icon=ft.icons.CHECK,
                    text=_("Check installation"),
                    on_click=self.on_click_check_installation,
                ),
                ft.ElevatedButton(
                    icon=ft.icons.LINK,
                    text=_("Create/Update shortcut"),
                    tooltip=_("Create or update ParaCopy desktop shortcut."),
                    on_click=self.on_click_create_or_update_shortcut,
                ),
                ft.Text(
                    _("Global settings"),
                    theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                ),
                ft.Row(
                    [
                        ft.Text("Language"),
                        ft.Dropdown(
                            value=self.settings.locale,
                            options=[
                                ft.dropdown.Option(key="system", text=_("System")),
                                ft.dropdown.Option(key="en", text="English"),
                                ft.dropdown.Option(key="fr", text="Français"),
                            ],
                            on_change=self.on_locale_change,
                        ),
                        ft.IconButton(
                            icon=ft.icons.INFO,
                            icon_color="black",
                            tooltip=_("Language is updated after restart."),
                        ),
                    ],
                ),
                ft.Text(
                    _("Copy settings"),
                    theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                ),
                ft.Row(
                    [
                        self.copy_num_destinations_per_process_field,
                        ft.IconButton(
                            icon=ft.icons.INFO,
                            icon_color="black",
                            tooltip=_(
                                "Number of destinations per copy process:\n"
                                "- 0: a single process for all destinations.\n"
                                "- 1 (2, 3, ...): 1 (2, 3, ...) destinations "
                                "per copy process.\n"
                                "More destinations per process increases copy speed, "
                                "but if there are faulty destinations, this may cause "
                                "errors.",
                            ),
                        ),
                    ],
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
        )

    def on_click_save(self, _event: ft.ControlEvent) -> None:
        """Handle when user clicks on the save button.

        Args:
        ----
            _event (ft.ControlEvent): unused

        """
        page = self.page
        self.settings_service.save(self.settings)

        def close_banner() -> None:
            page.banner.open = False
            page.update()

        page.banner = success_banner(_("Settings have been saved."), close_banner)
        page.banner.open = True
        page.update()

    def on_click_check_installation(self, _event: ft.ControlEvent) -> None:
        """Handle when user clicks on the check installation button.

        Args:
        ----
            _event (ft.ControlEvent): unused

        """
        self.page.go("/installation-check")

    def on_click_create_or_update_shortcut(self, _event: ft.ControlEvent) -> None:
        """Handle when user wants to create or update desktop shortcut.

        Args:
        ----
            _event (ft.ControlEvent): unused

        """
        page = self.page

        shortcut_service = ShortcutService()
        shortcut_service.create_or_update_shortcut()

        def close_banner() -> None:
            page.banner.open = False
            page.update()

        page.banner = success_banner(
            _("The shortcut has been created/updated."), close_banner
        )
        page.banner.open = True
        page.update()

    def on_locale_change(self, event: ft.ControlEvent) -> None:
        """Handle when use changes locale.

        Args:
        ----
            event (ft.ControlEvent): event

        """
        locale = event.data
        if locale is not None:
            self.settings.locale = locale

    def on_copy_num_destinations_per_process_change(
        self,
        event: ft.ControlEvent,
    ) -> None:
        """Handle when user changes num_destinations_per_process.

        Args:
        ----
            event (ft.ControlEvent): event

        """
        copy_num_destinations_per_process = event.data

        if (
            str.isdigit(copy_num_destinations_per_process)
            and int(copy_num_destinations_per_process) >= 0
        ):
            self.settings.copy_num_destinations_per_process = int(
                copy_num_destinations_per_process,
            )
            self.copy_num_destinations_per_process_field.error_text = None
        else:
            self.copy_num_destinations_per_process_field.error_text = _(
                "Must be greater or equal than 0",
            )
        self.update()
