"""View to display installation check step.

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

from typing import Literal

import flet as ft

StepState = Literal["idle", "checking", "success", "error", "warning"]


class StepView(ft.Container):
    """View to display installation check step."""

    def __init__(
        self,
        description: str,
        action: ft.Control | None = None,
    ) -> None:
        """Build StepView.

        Args:
        ----
            description (str): description of step
            action (ft.Control | None): optional action

        """
        super().__init__()

        # Model
        self.state: StepState = "idle"

        # View
        self.icon = ft.Icon(name=ft.icons.QUESTION_MARK, size=20, color=ft.colors.GREY)
        self.loading = ft.ProgressRing(height=20, width=20, visible=False)
        self.description_text = ft.Text(
            value=description,
            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
        )
        self.explanation_text = ft.Text(
            visible=False,
            theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
            selectable=True,
        )
        self.content = ft.Row(
            controls=[
                ft.Stack([self.icon, self.loading]),
                ft.Column(
                    [self.description_text, self.explanation_text],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    spacing=0,
                ),
                *([action] if action is not None else []),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

    def set_state(self, new_state: StepState) -> None:
        """Change state.

        Args:
        ----
            new_state (StepState): new state

        """
        match self.state:
            case "loading":
                self.loading.visible = False
                self.icon.visible = True

        self.state = new_state

        match self.state:
            case "idle":
                self.icon.name = ft.icons.QUESTION_MARK
                self.icon.color = ft.colors.GREY
                self.description_text.color = ft.colors.BLACK
                self.explanation_text.color = ft.colors.BLACK
            case "loading":
                self.loading.visible = True
                self.icon.visible = False
                self.description_text.color = ft.colors.BLACK
                self.explanation_text.color = ft.colors.BLACK
            case "warning":
                self.icon.name = ft.icons.WARNING
                self.icon.color = ft.colors.AMBER
                self.description_text.color = ft.colors.AMBER
                self.explanation_text.color = ft.colors.AMBER
            case "error":
                self.icon.name = ft.icons.ERROR
                self.icon.color = ft.colors.RED
                self.description_text.color = ft.colors.RED
                self.explanation_text.color = ft.colors.RED
            case "success":
                self.icon.name = ft.icons.CHECK
                self.icon.color = ft.colors.GREEN
                self.description_text.color = ft.colors.BLACK
                self.explanation_text.color = ft.colors.BLACK

        self.update()

    def set_explanation(self, explanation: str | None) -> None:
        """Set explanation.

        Args:
        ----
            explanation (str): explanation to display.

        """
        self.explanation_text.value = explanation
        self.explanation_text.visible = explanation is not None
        self.update()
