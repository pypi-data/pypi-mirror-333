"""Main view for About page.

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
from _version import __version__

COPYRIGHT_TEXT = _(
    """
# ParaCopy
**{version}**
[Release Notes](https://codeberg.org/paracopy/paracopy/releases) &
[Source Code](https://codeberg.org/paracopy/paracopy)

Copyright (c) 2024 Pierre-Yves Genest.
""",
)

LICENSE_TEXT = _(
    """
ParaCopy is licensed under the Affero GNU General Public License version 3.

> ParaCopy is free software: you can redistribute it and/or modify it under the terms \
of the GNU Affero General Public License as published by the Free Software Foundation, \
version 3 of the License.
>
> ParaCopy is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY\
; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR \
PURPOSE. See the GNU Affero General Public License for more details.
>
> You should have received a copy of the GNU Affero General Public License along with \
ParaCopy. If not, see <https://www.gnu.org/licenses/>.

*All rights reserved on the ParaCopy name and logo.*
""",
)


class AboutView(ft.Container):
    """Main view for About page."""

    def __init__(self) -> None:
        """Construct AboutView."""
        super().__init__(expand=True)

        # View
        self.content = ft.Column(
            controls=[
                ft.Text(
                    _("About"),
                    theme_style=ft.TextThemeStyle.TITLE_LARGE,
                ),
                ft.Row(
                    [
                        ft.Image(src="/icon.svg", width=96),
                        ft.Markdown(
                            COPYRIGHT_TEXT.format(version=__version__),
                            selectable=False,
                            on_tap_link=lambda e: self.page.launch_url(e.data),
                        ),
                    ],
                ),
                ft.Markdown(
                    LICENSE_TEXT,
                    selectable=False,
                    on_tap_link=lambda e: self.page.launch_url(e.data),
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
        )
