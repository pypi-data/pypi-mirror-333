[[EN](README.md) | FR]

# ParaCopy

ParaCopy est un logiciel qui a pour but de faciliter la copie parallèle d'un 
dossier vers plusieurs destinations (clés USB ou cartes SD).
Actuellement, ParaCopy ne fonctionne qu'avec la distribution Linux Fedora.

## Installation

ParaCopy fonctionne avec Python 3. Assurez-vous qu'il est bien installé sur votre système.

Installez le package `paracopy` depuis PyPI :
```shell
pip3 install paracopy
```

Vous pouvez lancer `paracopy` avec la commande suivante :
```shell
paracopy
```

## Développement

*La procédure suivante n'a été testée que sur Fedora 40.*

Assurez-vous que les paquets de distribution suivants sont installés :
`coreutils, dcfldd, polkit, rsync, systemd-udev, util-linux, util-linux-core, xclip, zenity`.

Assurez-vous que `uv` (https://docs.astral.sh/uv/) est installé.

Créez un nouvel environnement virtuel et installez les dépendances :
```shell
uv sync
source .venv/bin/activate
```

Vous pouvez ensuite exécuter ParaCopy avec la commande suivante :
```shell
python3 src/main.py
```

## Construction et déploiement

Activez l'environnement virtuel :
```shell
source .venv/bin/activate
```

Tout d'abord, compilez les fichiers de traduction s'ils ont été modifiés :
```shell
python3 tasks/compile_translations.py --locales-directory="paracopy/locales"
```

Mettez à jour l'étiquette de version.

Pour construire le package `paracopy`, exécutez la commande suivante :
```shell
uv build
```

Pour télécharger le package `paracopy` sur PyPI, exécutez la commande suivante :
```shell
uv publish
```

## Licence

ParaCopy est sous licence Affero GNU General Public License version 3.

> ParaCopy est un logiciel libre : vous pouvez le redistribuer et/ou le modifier selon les termes de la Affero GNU General Public License telle que publiée par la Free Software Foundation, version 3 de la Licence.
> 
> ParaCopy est distribué dans l'espoir qu'il sera utile, mais SANS AUCUNE GARANTIE ; sans même la garantie implicite de VALEUR COMMERCIALE ou d'ADAPTATION A UN USAGE PARTICULIER. Voir la Affero GNU General Public License pour plus de détails.
> 
> Vous devriez avoir reçu une copie de la Affero GNU General Public License avec ParaCopy. Si ce n'est pas le cas, voir [https://www.gnu.org/licenses/]().

Nous informons le lecteur, qu'en accord avec la licence AGPL-3.0-only, nous avons ajouté des conditions supplémentaires pour restreindre l'utilisation du nom "ParaCopy" et du logo de ParaCopy.

> La présente licence n'autorise pas l'utilisation des noms, des marques, ou des noms de produits de ParaCopy, à l'exception de l'utilisation raisonnable et habituelle en précisant l'origine de l'œuvre et en reproduisant le contenu du fichier COPYING.md.