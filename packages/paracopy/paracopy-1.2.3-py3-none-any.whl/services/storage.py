"""Service for storage.

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

import os
from pathlib import Path


class StorageService:
    """Storage service."""

    def __init__(self) -> None:
        """Build StorageService."""
        self.data_folder = Path("~").expanduser() / ".paracopy"
        self.ensure_folder_exists(self.data_folder)

    def ensure_folder_exists(self, path: str) -> None:
        """Ensure folder exists.

        Args:
        ----
            path (str): path to folder

        """
        Path(path).mkdir(parents=True, exist_ok=True)

    def ensure_file_exists(self, path: str) -> None:
        """Ensure a file exists.

        Args:
        ----
            path (str): path to file

        """
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        if not Path(path).exists():
            os.mknod(path)

    @property
    def destinations_file(self) -> Path:
        """File to store destinations.

        Returns
        -------
            str: destination file

        """
        destinations_file = self.data_folder / "destinations.json"
        self.ensure_file_exists(destinations_file)
        return destinations_file

    @property
    def settings_file(self) -> Path:
        """File to store settings.

        Returns
        -------
            str: settings file

        """
        settings_file = self.data_folder / "settings.json"
        self.ensure_file_exists(settings_file)
        return settings_file

    @property
    def sources_folder(self) -> Path:
        """Folder to store application sources.

        Returns
        -------
            str: sources

        """
        sources_folder = self.data_folder / "sources"
        self.ensure_folder_exists(sources_folder)
        return sources_folder

    @property
    def root_folder(self) -> Path:
        """Get root folder for ParaCopy application.

        Returns
        -------
            str: root folder

        """
        return Path(__file__).parent.parent.parent.resolve()

    @property
    def src_folder(self) -> Path:
        """Get source folder for ParaCopy application.

        Returns
        -------
            str: source folder

        """
        return Path(__file__).parent.parent.resolve()

    @property
    def assets_folder(self) -> Path:
        """Get assets folder for ParaCopy application.

        Returns
        -------
            str: assets folder

        """
        return self.src_folder / "assets"

    @property
    def locales_folder(self) -> Path:
        """Get locales folder for ParaCopy application.

        Returns
        -------
            str: locales folder

        """
        return self.src_folder / "locales"
