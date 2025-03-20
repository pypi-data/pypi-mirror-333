"""Service for destinations.

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

from pathlib import Path

from model.destination import Destinations, Hub

from services.storage import StorageService


class DestinationsService:
    """Service for destinations."""

    def __init__(self) -> None:
        """Build DestinationsService."""
        self.storage_service = StorageService()

    def get_hubs(self) -> list[Hub]:
        """Get hubs.

        Returns
        -------
            List[Hub]: hubs

        """
        with Path(self.storage_service.destinations_file).open(
            encoding="utf-8",
        ) as file:
            try:
                return Destinations.model_validate_json(file.read()).hubs
            except ValueError:
                return []

    def save_hubs(self, hubs: list[Hub]) -> None:
        """Save hubs.

        Args:
        ----
            hubs (List[Hub]): hubs

        """
        with Path(self.storage_service.destinations_file).open(
            "w",
            encoding="utf-8",
        ) as file:
            file.write(Destinations(hubs=hubs).model_dump_json())
