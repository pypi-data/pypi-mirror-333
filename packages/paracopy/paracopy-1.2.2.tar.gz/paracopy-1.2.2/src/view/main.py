"""Main ParaCopy view.

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

from concurrent.futures import ThreadPoolExecutor

import flet as ft
from localization import _
from view.about.main import AboutView
from view.copy.main import CopyView
from view.hubs.main import HubsView
from view.installation.main import InstallationCheckView
from view.settings.main import SettingsView
from view.source.main import SourcesView


class MainView:
    """Main ParaCopy view."""

    def __init__(self, page: ft.Page) -> None:
        """Build MainView.

        Args:
        ----
            page (ft.Page): flet page

        """
        self.page = page
        self.set_title("ParaCopy")
        self.page.window_min_height = 600
        self.page.window_min_width = 700

        # Navigation rail
        self.rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            group_alignment=0,
            leading=ft.Image(src="/icon.svg", width=40),
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.DOWNLOAD_OUTLINED,
                    selected_icon=ft.icons.DOWNLOAD,
                    label=_("Copy"),
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.USB_OUTLINED,
                    selected_icon=ft.icons.USB,
                    label=_("Hubs"),
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.DRIVE_FOLDER_UPLOAD_OUTLINED,
                    selected_icon=ft.icons.DRIVE_FOLDER_UPLOAD_SHARP,
                    label=_("Sources"),
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SETTINGS_OUTLINED,
                    selected_icon=ft.icons.SETTINGS,
                    label=_("Settings"),
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.INFO_OUTLINED,
                    selected_icon=ft.icons.INFO,
                    label=_("About"),
                ),
            ],
            on_change=self.on_navigation_rail_change,
        )

        self.main = ft.Container(expand=True)
        self.page.add(
            ft.Row(
                [self.rail, ft.VerticalDivider(width=1), self.main],
                expand=True,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
        )
        self.page.update()

        # Startup
        self.page.starting = True
        self.page.on_route_change = self.on_route_change
        self.rail.selected_index = 0
        self.page.go("/installation-check")

        # Enable/Disable rail
        self.page.enable_rail = self.enable_rail

        # When user wants to leave application
        self.page.window_prevent_close = True
        self.page.on_window_event = self.on_window_event
        self.page.confirm_exit: str = None

        # Add thread execution
        self.page.thread_pool = ThreadPoolExecutor()
        self.page.run_thread_custom = self.page.thread_pool.submit

    def on_window_event(self, event: ft.ControlEvent) -> None:
        """Handle window event.

        Args:
        ----
            event (ft.ControlEvent): event

        """
        if event.data == "close":
            if self.page.confirm_exit is None:
                self.page.window_destroy()
            else:
                # Ask user for confirmation before closing
                def no_click(self: "MainView") -> None:
                    confirm_dialog.open = False
                    self.page.update()

                def yes_click(self: "MainView") -> None:
                    self.page.window_destroy()

                confirm_dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Text(_("Quit ParaCopy")),
                    content=ft.Text(
                        _("Do you want to quit ParaCopy?")
                        + " "
                        + self.page.confirm_exit,
                    ),
                    actions=[
                        ft.TextButton(_("Cancel"), on_click=no_click),
                        ft.TextButton(_("Quit"), on_click=yes_click),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
                self.page.dialog = confirm_dialog
                self.page.open(self.page.dialog)

    def on_route_change(self, event: ft.RouteChangeEvent) -> None:
        """Handle route change.

        Args:
        ----
            event (ft.RouteChangeEvent): event

        """
        if self.main.content is not None:
            self.main.content.clean()
        self.page.overlay.clear()
        self.page.update()

        route = event.route
        match route:
            case "/copy":
                self.route_copy()
            case "/hubs":
                self.route_hubs()
            case "/sources":
                self.route_sources()
            case "/settings":
                self.route_settings()
            case "/about":
                self.route_about()
            case "/installation-check":
                self.route_installation()

    def on_navigation_rail_change(self, event: ft.ControlEvent) -> None:
        """Handle click on navigation rail.

        Args:
        ----
            event (ft.ControlEvent): event

        """
        rail_index = int(event.data)
        match rail_index:
            case 0:  # Copy table
                self.page.go("/copy")
            case 1:  # Hub management
                self.page.go("/hubs")
            case 2:  # Source management
                self.page.go("/sources")
            case 3:  # Settings
                self.page.go("/settings")
            case 4:  # About
                self.page.go("/about")

    def enable_rail(self, *, enabled: bool) -> None:
        """Enable or Disable navigation rail.

        Args:
        ----
            enabled (bool): enabled state

        """
        self.rail.disabled = not enabled
        self.page.update()

    def route_copy(self) -> None:
        """Navigate to copy view."""
        self.set_title(_("ParaCopy — Copy Table"))
        self.main.content = CopyView()
        self.page.update()

    def route_sources(self) -> None:
        """Navigate to source management view."""
        self.set_title(_("ParaCopy — Source Management"))
        self.main.content = SourcesView()
        self.page.update()

    def route_hubs(self) -> None:
        """Navigate to hub management view."""
        self.set_title(_("ParaCopy — Hub Management"))
        self.main.content = HubsView()
        self.page.update()

    def route_settings(self) -> None:
        """Navigate to settings view."""
        self.set_title(_("ParaCopy — Settings"))
        self.main.content = SettingsView()
        self.page.update()

    def route_about(self) -> None:
        """Navigate to about view."""
        self.set_title(_("ParaCopy — About"))
        self.main.content = AboutView()
        self.page.update()

    def route_installation(self) -> None:
        """Navigate to installation check view."""
        self.set_title(_("ParaCopy — Installation Check"))
        self.main.content = InstallationCheckView()
        self.page.update()

    def set_title(self, title: str) -> None:
        """Update application title.

        Args:
        ----
            title (str): title

        """
        self.page.title = title
        self.page.update()
