"""Service to check ParaCopy installation.

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

import asyncio
import contextlib
import platform
import subprocess
import sys
from pathlib import Path
from typing import Literal

import aiohttp
import distro
from packaging.version import Version

from _version import __version__
from localization import _
from services.utils import async_subprocess_check_call, ensure_root

UpdateState = Literal["up-to-date", "outdated", "error"]

FEDORA_DEPENDENCIES = [
    "coreutils",
    "dcfldd",
    "polkit",
    "rsync",
    "systemd-udev",
    "util-linux",
    "util-linux-core",
    "xclip",
    "zenity",
]


class InstallationService:
    """Worker to check Operating system and install required packages."""

    def __init__(self) -> None:
        """Build InstallationWorker.

        Args:
        ----
            callback (Callable[[str], None]): callback to call after installation check

        """
        self.linux_distro = ""

    async def check_1_operating_system(self) -> tuple[bool, str | None]:
        """Check operating system.

        Returns
        -------
            bool, str | None: if check is successful + optional explanation

        """
        operating_system = platform.system()
        if operating_system == "Linux":
            return True, None
        return False, _("ParaCopy is only working with Linux.")

    async def check_2_distribution(self) -> tuple[bool, str | None]:
        """Check Linux distribution.

        Returns
        -------
            bool, str | None: if check is successful + optional explanation

        """
        self.linux_distro = distro.id()
        try:
            distro_version = int(distro.major_version())
        except ValueError:
            distro_version = -1

        if self.linux_distro == "fedora":
            if distro_version >= 40:
                return True, None
            return False, _("ParaCopy support only Fedora ≥ 40.").format(
                distro=self.linux_distro,
            )

        return (
            False,
            _("ParaCopy does not support '{distro} {version}'.").format(
                distro=self.linux_distro,
                version=distro_version,
            ),
        )

    async def check_3_pkexec_fedora(self) -> tuple[bool, str | None]:
        """Check if pkexec is available (Fedora).

        Returns
        -------
            bool, str | None: if check is successful + optional explanation

        """
        if Path("/usr/bin/pkexec").is_file():
            return True, None
        return (
            False,
            _(
                "The command pkexec is not available. Please install the polkit "
                "package.\n"
                "You can use the following command: `sudo dnf install polkit`.",
            ),
        )
        return False

    async def check_3_pkexec(self) -> tuple[bool, str | None]:
        """Check if pkexec is available.

        Returns
        -------
            bool, str | None: if check is successful + optional explanation

        """
        match self.linux_distro:
            case "fedora":
                return await self.check_3_pkexec_fedora()
            case _:
                return False, _("Unknown error.")

    async def check_4_packages_fedora(self) -> tuple[bool, str | None]:
        """Check if required packages are installed (Fedora).

        Returns
        -------
            bool, str | None: if check is successful + optional explanation

        """
        with contextlib.suppress(Exception):
            await async_subprocess_check_call(
                "/usr/bin/rpm",
                "-q",
                *FEDORA_DEPENDENCIES,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
            return True, None
        return (
            False,
            _("Some packages are missing: `{packages}`.\nPlease install them.").format(
                packages=", ".join(FEDORA_DEPENDENCIES),
            ),
        )

    async def check_4_packages(self) -> tuple[bool, str | None]:
        """Check if required packages are installed.

        Returns
        -------
            bool, str | None: if check is successful + optional explanation

        """
        match self.linux_distro:
            case "fedora":
                return await self.check_4_packages_fedora()
            case _:
                return False, _("Unknown error.")

    async def install_4_packages_fedora(self) -> tuple[bool, str | None]:
        """Install the missing packages (Fedora).

        Returns
        -------
            bool, str | None: if installation is successful + optional explanation

        """
        with contextlib.suppress(Exception):
            await async_subprocess_check_call(
                *ensure_root(["/usr/bin/dnf", "install", "-y", *FEDORA_DEPENDENCIES]),
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
            return True, None

        return (
            False,
            _("Unable to install the required packages: `{packages}`.").format(
                packages=", ".join(FEDORA_DEPENDENCIES),
            ),
        )

    async def install_4_packages(self) -> tuple[bool, str | None]:
        """Install the missing packages.

        Returns
        -------
            bool, str | None: if check is successful + optional explanation

        """
        match self.linux_distro:
            case "fedora":
                return await self.install_4_packages_fedora()
            case _:
                return False, _("Unknown error.")

    async def check_5_update(self) -> tuple[UpdateState, str | None]:
        """Check if paracopy is up to date.

        Returns
        -------
            tuple[UpdateState, str | None]: if paracopy is
                up to date + optional explanation

        """
        try:
            async with (
                aiohttp.ClientSession() as session,
                session.get("https://pypi.org/pypi/paracopy/json") as response,
            ):
                package_information = await response.json()
                pypi_version = package_information["info"]["version"]

                if Version(pypi_version) > Version(__version__):
                    return "outdated", _(
                        "New version {version} of ParaCopy is available. "
                        "Please install it.",
                    ).format(version=pypi_version)

                return "up-to-date", None
        except aiohttp.ClientResponseError:
            return "error", _("Unable to request PyPI.")
        except (aiohttp.ContentTypeError, ValueError):
            return "error", _("PyPI does not return the correct format.")

    def install_5_update(self) -> None:
        """Install newer version of ParaCopy."""
        subprocess.Popen(
            [sys.executable, "-m", "pip", "install", "paracopy", "--upgrade"],
            start_new_session=True,
        )
        sys.exit(0)
