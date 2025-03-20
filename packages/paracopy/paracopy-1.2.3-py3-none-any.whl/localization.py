"""Localization.

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

import gettext
import locale

from model.settings import LOCALES_CHOICES
from services.settings import SettingsService
from services.storage import StorageService

settings_service = SettingsService()
settings = settings_service.load()
storage_service = StorageService()
locales_folder = storage_service.locales_folder

# Find locale
user_locale = settings.locale  # Settings defined locale
system_locale = locale.getlocale()[0]  # System defined locale

# Define locale
DEFAULT_LOCALES = {
    "en": "en_US",
    "fr": "fr_FR",
}
__locale__: str = ""
if user_locale == "system":
    __locale__ = system_locale
elif user_locale in LOCALES_CHOICES:
    if system_locale.startswith(f"{user_locale}_"):
        __locale__ = system_locale
    else:
        __locale__ = DEFAULT_LOCALES[user_locale]

# Define translation
translation_name = __locale__.split("_")[0]
if translation_name in LOCALES_CHOICES.difference(["en"]):
    translation = gettext.translation(
        "paracopy",
        locales_folder,
        languages=[translation_name],
    )
    translation.install()
    _ = translation.gettext
    N_ = translation.ngettext
else:
    _ = gettext.gettext
    N_ = gettext.ngettext

__byte_unit_length__ = ""
match translation_name:
    case "fr":
        __byte_unit_length__ = "short"
    case "en":
        __byte_unit_length__ = "narrow"
