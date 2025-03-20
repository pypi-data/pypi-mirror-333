# syspathmodif

## FRANÇAIS

Cette bibliothèque offre des manières concises de modifier la liste `sys.path`.
L'utilisateur ne devrait pas avoir besoin d'interagir directement avec cette
liste.

### Contenu

Les fonctions suivantes prennent un chemin de type `str` ou `pathlib.Path`
comme argument. Elles convertissent les arguments de type `pathlib.Path` en
`str` puisque `sys.path` n'est censée contenir que des chaînes de caractères.

* `sp_append` ajoute le chemin donné à la fin de `sys.path`.
* `sp_contains` indique si `sys.path` contient le chemin donné.
* `sp_prepend` ajoute le chemin donné au début de `sys.path`.
* `sp_remove` enlève le chemin donné de `sys.path`.

Au moment de sa création, une instance de `SysPathBundle` contient plusieurs
chemins et les ajoute au début de `sys.path`. Quand on vide (*clear*) une
instance, elle efface son contenu et l'enlève de `sys.path`. Ainsi, cette
classe facilite l'ajout et le retrait d'un groupe de chemins.

Il est possible d'utiliser `SysPathBundle` comme un gestionnaire de contexte
(*context manager*). Dans ce cas, l'instance est vidée à la fin du bloc `with`.

La fonction `sm_contains` prend comme argument un nom (`str`) de module ou de
paquet. Elle indique si le dictionnaire `sys.modules` contient ce module ou
paquet.

Pour plus d'informations, consultez la documentation et les démos dans le dépôt
de code source.

### Importations et `sys.path`

Il est possible d'importer un module ou un paquet si la liste `sys.path`
contient le chemin de son dossier parent. On peut donc rendre un module ou un
paquet importable en ajoutant son chemin parent à `sys.path`.

### Importations et `sys.modules`

Le dictionnaire `sys.modules` associe des noms (`str`) de module ou de paquet
au module ou paquet correspondant. Le système d'importation l'utilise comme
cache; tout module ou paquet importé pour la première fois y est ajouté.
Puisque le système d'importation cherche d'abord les modules et paquets
demandés dans `sys.modules`, les modules et paquets qu'il contient peuvent être
importés partout sans qu'on modifie `sys.path`.

Sachant cela, on peut déterminer à l'aide de la fonction `sm_contains` si un
module ou un paquet est déjà importable. Si `sm_contains` renvoie vrai
(`True`), il n'est pas nécessaire de modifier `sys.path` pour importer le
module ou le paquet donné.

### Dépendances

Installez les dépendances de `syspathmodif` avant de l'utiliser.
```
pip install -r requirements.txt
```

Cette commande installe les dépendances de développement en plus des
dépendances ordinaires.
```
pip install -r requirements-dev.txt
```

### Démos

Les scripts dans le dossier `demos` montrent comment `syspathmodif` permet
d'importer un module ou un paquet qui est indisponible tant qu'on n'a pas
ajouté son chemin parent à `sys.path`. Toutes les démos dépendent du paquet
`demo_package`.

`demo_functions.py` ajoute la racine du dépôt à `sys.path` à l'aide de la
fonction `sp_prepend`. Après les importations, la démo annule cette
modification à l'aide de la fonction `sp_remove`.
```
python demos/demo_functions.py
```

`demo_bundle.py` ajoute la racine du dépôt et le dossier `demo_package` à
`sys.path` à l'aide de la classe `SysPathBundle`. Après les importations, la
démo annule ces modifications en vidant l'instance de `SysPathBundle`.
```
python demos/demo_bundle.py
```

`demo_bundle_context.py` effectue la même tâche que `demo_bundle.py` en
utilisant `SysPathBundle` comme un gestionnaire de contexte.
```
python demos/demo_bundle_context.py
```

`demo_sm_contains1.py` montre un cas où on peut importer un module ou un paquet
sans ajouter son chemin parent à `sys.path`. La démo vérifie la présence du
module ou du paquet dans `sys.modules` à l'aide de la fonction `sm_contains`.
```
python demos/demo_sm_contains1.py
```

`demo_sm_contains2.py` montre un autre usage de la fonction `sm_contains`.
```
python demos/demo_sm_contains2.py
```

### Tests automatiques

Cette commande exécute les tests automatiques.
```
pytest tests
```

## ENGLISH

This library offers concise manners to modify list `sys.path`.
The user should not need to directly interact with that list.

### Content

The following functions take a path of type `str` or `pathlib.Path` as an
argument. They convert arguments of type `pathlib.Path` to `str` since
`sys.path` is supposed to contain only character strings.

* `sp_append` adds the given path to the end of `sys.path`.
* `sp_contains` indicates whether `sys.path` contains the given path.
* `sp_prepend` adds the given path to the beginning of `sys.path`.
* `sp_remove` removes the given path from `sys.path`.

Upon creation, a `SysPathBundle` instance stores several paths and prepends
them to `sys.path`. When a bundle is cleared, it erases its content and removes
it from `sys.path`. Thus, this class facilitates adding and removing a group of
paths.

`SysPathBundle` can be used as a context manager. In that case, the instance is
cleared at the `with` block's end.

Function `sm_contains` takes a module's or package's name (`str`) as an
argument. It indicates whether dictionary `sys.modules` contains the module or
package.

For more information, consult the documentation and the demos in the source
code repository.

### Imports and `sys.path`

It is possible to import a module or package if list `sys.path` contains the
path to its parent directory. Therefore, you can make a module or package
importable by adding its parent path to `sys.path`.

### Imports and `sys.modules`

Dictionary `sys.modules` maps module and package names (`str`) to the
corresponding module or package. The import system uses it as a cache; any
module or package imported for the first time is stored in it. Since the import
system looks for the requested modules and packages in `sys.modules` first, the
modules and packages that it contains can be imported everywhere with no
modifications to `sys.path`.

Knowing this, you can use function `sm_contains` to determine if a module or
package is already importable. If `sm_contains` returns `True`, modifiying
`sys.path` is not required to import the given module or package.

### Dependencies

Install the dependencies before using `syspathmodif`.
```
pip install -r requirements.txt
```

This command installs the development dependencies in addition to the ordinary
dependencies.
```
pip install -r requirements-dev.txt
```

### Demos

The scripts in directory `demos` show how `syspathmodif` allows to import a
module or package unavailable unless its parent path is added to `sys.path`.
All demos depend on `demo_package`.

`demo_functions.py` adds the repository's root to `sys.path` with function
`sp_prepend`. After the imports, the demo undoes this modification with
function `sp_remove`.
```
python demos/demo_functions.py
```

`demo_bundle.py` adds the repository's root and `demo_package` to `sys.path`
with class `SysPathBundle`. After the imports, the demo undoes these
modifications by clearing the `SysPathBundle` instance.
```
python demos/demo_bundle.py
```

`demo_bundle_context.py` performs the same task as `demo_bundle.py` by using
`SysPathBundle` as a context manager.
```
python demos/demo_bundle_context.py
```

`demo_sm_contains1.py` shows a case where a module or package can be imported
without its parent path being added to `sys.path`. The demo verifies the
module's or package's presence in `sys.modules` with function `sm_contains`.
```
python demos/demo_sm_contains1.py
```

`demo_sm_contains2.py` shows another use of function `sm_contains`.
```
python demos/demo_sm_contains2.py
```

### Automated Tests

This command executes the automated tests.
```
pytest tests
```
