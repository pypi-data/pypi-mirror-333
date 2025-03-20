"""Service for Settings.

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

from pathlib import Path

from model.settings import Settings
from services.storage import StorageService


class SettingsService:
    """Service to manage settings."""

    def __init__(self) -> None:
        """Build SettingsService."""
        self.storage_service = StorageService()

    def load(self) -> Settings:
        """Load settings.

        Returns
        -------
            Settings: settings

        """
        with Path(self.storage_service.settings_file).open(encoding="utf-8") as file:
            try:
                return Settings.model_validate_json(file.read())
            except ValueError:
                return Settings()

    def save(self, settings: Settings) -> None:
        """Save settings.

        Args:
        ----
            settings (Settings): settings

        """
        with Path(self.storage_service.settings_file).open(
            "w",
            encoding="utf-8",
        ) as file:
            file.write(settings.model_dump_json())
