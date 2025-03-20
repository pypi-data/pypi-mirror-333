"""Main view for sources management.

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

from localization import _
from view.source.creation import SourceCreationView
from view.source.list import SourceListView


class SourcesView(ft.Container):
    """Main view for sources management."""

    def __init__(self) -> None:
        """Build SourcesView."""
        super().__init__(expand=True)
        self.content = ft.Column(
            controls=[
                ft.Text(_("Your sources"), theme_style=ft.TextThemeStyle.TITLE_LARGE),
                SourceListView(),
                ft.Text(
                    _("Create a source"),
                    theme_style=ft.TextThemeStyle.TITLE_LARGE,
                ),
                SourceCreationView(),
            ],
            alignment=ft.MainAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
        )
