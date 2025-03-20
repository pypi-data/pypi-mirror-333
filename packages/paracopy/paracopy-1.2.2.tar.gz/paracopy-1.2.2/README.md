[EN | [FR](https://gitlab.com/paracopy/paracopy/-/blob/main/README.fr.md)]

# ParaCopy

ParaCopy is a software that aims to facilitate the parallel copy of a folder 
to multiple destinations (USB disks or SD cards).
Currently, ParaCopy only supports the Fedora Linux distribution.

## Install

ParaCopy is Python package.
Ensure that Python 3 is installed on your computer.

Install the `paracopy` package from PyPI:
```shell
pip3 install paracopy
```

You can then run `paracopy` with the command:
```shell
paracopy
```

## Development

*The following procedure has only been tested on Fedora 40.*

Ensure that the following distribution packages are installed:
`coreutils, dcfldd, polkit, rsync, systemd-udev, util-linux, util-linux-core, xclip, zenity`.

Ensure that `uv` (https://docs.astral.sh/uv/) is installed.

Create a new venv and install the requirements:
```shell
uv sync
source .venv/bin/activate
```

You can then run ParaCopy with the following command:
```shell
python3 src/main.py
```

## Build and deployment

Activate the venv:
```shell
source .venv/bin/activate
```

First, compile the translation files if they were modified:
```shell
python3 tasks/compile_translations.py --locales-directory="paracopy/locales"
```

Update the version tag.

To build the `paracopy` package, run the following command:
```shell
uv build
```

To upload the `paracopy` package to PyPI, run the following command:
```shell
uv publish
```

## License

ParaCopy is licensed under the Affero GNU General Public License version 3.


> ParaCopy is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, version 3 of the License.
> 
> ParaCopy is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
> 
> You should have received a copy of the GNU Affero General Public License along with ParaCopy. If not, see <https://www.gnu.org/licenses/>.


We inform the reader that, in accordance with the AGPL-3.0-only license,
additional terms have been added to restrict the use of the name "ParaCopy"
and the logo of ParaCopy.

> This License does not grant permission to use the trade names, trademarks, service marks, or product names of the Licensor, except as required for reasonable and customary use in describing the origin of the Work and reproducing the content of the COPYING.md file.