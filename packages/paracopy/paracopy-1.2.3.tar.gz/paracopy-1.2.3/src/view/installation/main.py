"""Main view for installation check.

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

import asyncio

import flet as ft

from localization import _
from services.installation import InstallationService
from view.installation.step import StepView


class InstallationCheckView(ft.Container):
    """Main view for installation check."""

    def __init__(self) -> None:
        """Build InstallationCheckView."""
        super().__init__(expand=True)

        # Model
        self.installation_service = InstallationService()
        self.waiting_lock = asyncio.Event()

        # View
        self.check_button = ft.FilledButton(
            icon=ft.icons.CHECK,
            text=_("Check now"),
            on_click=self.on_click_check_installation,
        )
        self.step_4_packages_install_button = ft.TextButton(
            _("Install missing"),
            on_click=self.on_set_unlock_wait,
            visible=False,
        )
        self.step_5_update_install_button = ft.TextButton(
            _("Update now"),
            on_click=self.on_set_unlock_wait,
            visible=False,
        )
        self.step_1_operating_system = StepView(_("Operating system is Linux."))
        self.step_2_distribution = StepView(_("Linux distribution is supported."))
        self.step_3_pkexec = StepView(_("pkexec is installed."))
        self.step_4_packages = StepView(
            _("Required packages are installed."),
            self.step_4_packages_install_button,
        )
        self.step_5_update = StepView(
            _("ParaCopy is up-to-date."),
            self.step_5_update_install_button,
        )
        self.content = ft.Column(
            controls=[
                ft.Row(
                    [
                        ft.Text(
                            _("Installation Check"),
                            theme_style=ft.TextThemeStyle.TITLE_LARGE,
                            expand=True,
                        ),
                        self.check_button,
                    ],
                ),
                self.step_1_operating_system,
                self.step_2_distribution,
                self.step_3_pkexec,
                self.step_4_packages,
                self.step_5_update,
            ],
            alignment=ft.MainAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
        )

    def did_mount(self) -> None:
        """Launch automatically check at startup."""
        if self.page.starting:
            self.on_click_check_installation()

    def on_set_unlock_wait(self, _event: ft.ControlEvent | None = None) -> None:
        """Unlock waiting lock.

        Args:
        ----
            _event (ft.ControlEvent | None, optional): unused. Defaults to None.

        """
        self.waiting_lock.set()

    def on_click_check_installation(
        self,
        _event: ft.ControlEvent | None = None,
    ) -> None:
        """Handle when user wants to check installation.

        Args:
        ----
            _event (ft.ControlEvent | None, optional): unused

        """
        self.page.run_task(self.check_installation)

    async def check_installation(self) -> None:
        """Check installation."""
        self.page.enable_rail(enabled=False)
        self.check_button.disabled = True
        self.update()

        if not await self.check_1_operating_system():
            return

        if not await self.check_2_distribution():
            return

        if not await self.check_3_pkexec():
            return

        if not await self.check_4_packages():
            return

        self.page.enable_rail(enabled=True)
        self.update()

        # User can dismiss update
        if not await self.check_5_update():
            return

        self.check_button.disabled = False
        self.update()

        if self.page.starting:
            self.page.starting = False
            self.page.go("/copy")

    async def check_1_operating_system(self) -> bool:
        """Check if operating system is correct.

        Returns
        -------
            bool: if check is successful.

        """
        (
            success,
            explanation,
        ) = await self.installation_service.check_1_operating_system()

        if success:
            self.step_1_operating_system.set_state("success")
        else:
            self.step_1_operating_system.set_state("error")
            self.step_1_operating_system.set_explanation(explanation)

        return success

    async def check_2_distribution(self) -> bool:
        """Check if Linux distribution is correct.

        Returns
        -------
            bool: if check is successful.

        """
        (
            success,
            explanation,
        ) = await self.installation_service.check_2_distribution()

        if success:
            self.step_2_distribution.set_state("success")
        else:
            self.step_2_distribution.set_state("error")
            self.step_2_distribution.set_explanation(explanation)

        return success

    async def check_3_pkexec(self) -> bool:
        """Check if pkexec is installed.

        Returns
        -------
            bool: if check is successful.

        """
        (
            success,
            explanation,
        ) = await self.installation_service.check_3_pkexec()

        if success:
            self.step_3_pkexec.set_state("success")
        else:
            self.step_3_pkexec.set_state("error")
            self.step_3_pkexec.set_explanation(explanation)

        return success

    async def check_4_packages(self) -> bool:
        """Check if required packages are installed.

        Returns
        -------
            bool: if check is successful.

        """
        (
            success,
            explanation,
        ) = await self.installation_service.check_4_packages()

        if success:
            self.step_4_packages.set_state("success")
            return success

        # Missing packages
        self.step_4_packages.set_state("warning")
        self.step_4_packages.set_explanation(explanation)
        self.step_4_packages_install_button.visible = True
        self.update()

        self.waiting_lock.clear()
        await self.waiting_lock.wait()  # Wait user click button
        self.step_4_packages_install_button.visible = False
        self.step_4_packages.set_state("loading")
        self.update()

        (
            success,
            explanation,
        ) = await self.installation_service.install_4_packages()

        if success:
            self.step_4_packages.set_state("success")
            self.step_4_packages.set_explanation(None)
        else:
            self.step_4_packages.set_state("error")
            self.step_4_packages.set_explanation(explanation)

        return success

    async def check_5_update(self) -> bool:
        """Check if ParaCopy is up-to-date.

        Returns
        -------
            bool: if check is successful.

        """
        (
            success,
            explanation,
        ) = await self.installation_service.check_5_update()

        match success:
            case "error":
                self.step_5_update.set_state("error")
                self.step_5_update.set_explanation(explanation)
                return False
            case "up-to-date":
                self.step_5_update.set_state("success")
                return True

        # New version is available
        self.step_5_update.set_state("warning")
        self.step_5_update.set_explanation(explanation)
        self.step_5_update_install_button.visible = True
        self.update()

        self.waiting_lock.clear()
        await self.waiting_lock.wait()  # Wait user click button
        self.step_5_update_install_button.visible = False
        self.step_5_update.set_state("loading")
        self.update()

        (
            success,
            explanation,
        ) = await self.installation_service.install_5_update()

        if success:
            self.step_5_update.set_state("success")
            self.step_5_update.set_explanation(None)
        else:
            self.step_5_update.set_state("error")
            self.step_5_update.set_explanation(explanation)

        return success
