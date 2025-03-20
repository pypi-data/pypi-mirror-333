"""Task to compile PO translations into MO files.

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
import os
import subprocess
from pathlib import Path


def main(locales_directory: str) -> None:
    """Run script.

    Args:
    ----
        locales_directory (str): folder to locales

    """
    for locale in os.listdir(locales_directory):
        if Path(f"{locales_directory}/{locale}").is_dir():
            subprocess.check_call(
                [
                    "/usr/bin/msgfmt",
                    "--check",
                    f"--output-file={locales_directory}/{locale}/LC_MESSAGES/paracopy.mo",
                    f"{locales_directory}/{locale}/LC_MESSAGES/paracopy.po",
                ],
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Compile Translations",
        description="Script to compile translation files",
    )
    parser.add_argument(
        "--locales-directory",
        help="Path to locales",
        type=str,
        required=True,
    )
    parser_args = parser.parse_args()

    main(parser_args.locales_directory)
