"""Main service to create or update paracopy shortcut.

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

import sys
from pathlib import Path
from string import Template

from services.storage import StorageService


class ShortcutService:
    """Main service to create or update paracopy shortcut."""

    def __init__(self) -> None:
        """Build ShortcutService."""
        self.storage_service = StorageService()

    def create_or_update_shortcut(self) -> None:
        """Create or update desktop entry."""
        # Get desktop entry template
        with Path(f"{self.storage_service.assets_folder}/paracopy.desktop").open(
            encoding="utf-8",
        ) as file:
            desktop_entry_template = Template(file.read())

        # Create desktop entry folder if needed
        desktop_entry_folder = Path.home() / ".local/share/applications"
        desktop_entry_folder.mkdir(exist_ok=True, parents=True)

        # Write desktop entry
        with Path(f"{desktop_entry_folder}/paracopy.desktop").open(
            "w",
            encoding="utf-8",
        ) as file:
            desktop_entry = desktop_entry_template.substitute(
                {
                    "icon_path": f"{self.storage_service.assets_folder}/icon.svg",
                    "python_path": sys.executable,
                    "paracopy_folder": self.storage_service.root_folder,
                },
            )
            file.write(desktop_entry)
