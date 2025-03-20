"""Task to update PO translation files.

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

import argparse
import pathlib
import subprocess
from pathlib import Path


def main(locales_directory: str, locales: list[str], source_directory: str) -> None:
    """Run update script.

    Args:
    ----
        locales_directory (str): folder to locales
        locales (List[str]): locales codes
        source_directory (str): folder containing source files

    """
    # Generate template POT with translations
    source_files = list(pathlib.Path(source_directory).rglob("*.py"))
    subprocess.check_call(
        [
            "/usr/bin/xgettext",
            "--force-po",
            "-F",
            f"--output={locales_directory}/paracopy.pot",
            "--strict",
            "--package-name=paracopy",
            "--copyright-holder=Pierre-Yves Genest",
            *source_files,
        ],
    )

    # Create/Merge corresponding PO files
    for locale in locales:
        if Path(f"{locales_directory}/{locale}/LC_MESSAGES/paracopy.po").exists():
            subprocess.check_call(
                [
                    "/usr/bin/msgmerge",
                    f"--output-file={locales_directory}/{locale}/LC_MESSAGES/paracopy.po",
                    f"{locales_directory}/{locale}/LC_MESSAGES/paracopy.po",
                    f"{locales_directory}/paracopy.pot",
                ],
            )
        else:
            subprocess.check_call(
                [
                    "/usr/bin/msginit",
                    f"--input={locales_directory}/paracopy.pot",
                    f"--output-file={locales_directory}/{locale}/LC_MESSAGES/paracopy.po",
                    f"--locale={locale}",
                ],
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Update Translations",
        description="Script to generate/update translation files",
    )
    parser.add_argument(
        "--locales-directory",
        help="Path to locales",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--locales",
        help="Locale code (e.g., fr, de, ...)",
        type=lambda locales: locales.split(","),
        required=True,
    )
    parser.add_argument(
        "--source-directory",
        help="Path to source files (to identify strings that need translation)",
        type=str,
        required=True,
    )
    parser_args = parser.parse_args()

    main(
        parser_args.locales_directory,
        parser_args.locales,
        parser_args.source_directory,
    )
