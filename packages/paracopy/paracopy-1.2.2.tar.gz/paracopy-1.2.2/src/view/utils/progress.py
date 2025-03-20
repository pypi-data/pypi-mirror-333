"""Progress bar that display an estimated time left.

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

from datetime import datetime, timezone

import flet as ft
from babel.dates import format_timedelta
from localization import _, __locale__


class TimerProgressBar(ft.Column):
    """Progress bar that display an estimated time left."""

    def __init__(self, *args, **kwargs) -> None:
        """Build TimerProgressBar."""
        super().__init__(*args, **kwargs)

        self.progress = ft.ProgressBar()
        self.progress_text = ft.Text(
            None,
            width=200,
            theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
        )
        self.controls = [
            self.progress_text,
            self.progress,
        ]

        self.start = None

    @property
    def value(self) -> float:
        """Get value of progress bar.

        Returns
        -------
            float: value

        """
        return self.progress.value

    @value.setter
    def value(self, value: float | None = None) -> None:
        """Set value of progress bar.

        Args:
        ----
            value (float, optional): value. Defaults to .0.

        """
        if value is None:
            self.start = None
            self.progress.value = None
            self.progress_text.value = None
            self.update()
            return

        value = max(0.0, min(1.0, value))
        if value == 0.0:
            self.start = datetime.now(tz=timezone.utc)
            self.progress.value = 0
            self.progress_text.value = _("Remaining time: undetermined")
        else:
            self.progress.value = value

            if self.start is not None:
                elapsed_time = datetime.now(tz=timezone.utc) - self.start
                estimated_time_left = (1 - value) / value * elapsed_time
                self.progress_text.value = _(
                    "Remaining time: {estimated_time_left}",
                ).format(
                    estimated_time_left=format_timedelta(
                        estimated_time_left,
                        locale=__locale__,
                    ),
                )
        self.update()
