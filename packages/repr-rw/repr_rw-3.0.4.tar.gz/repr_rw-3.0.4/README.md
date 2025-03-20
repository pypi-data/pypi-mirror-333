# repr_rw

## FRANÇAIS

Cette bibliothèque écrit des représentations d'objets dans un fichier texte et
lit le fichier pour recréer les objets. Une représentation d'objet est une
chaîne de caractères renvoyée par la fonction `repr`.

### Contenu

La fonction `write_reprs` écrit des représentations d'objets dans un fichier
texte. Chaque ligne du fichier est une représentation d'objet. Si le fichier
spécifié existe déjà, cette fonction l'écrase.

Le générateur `read_reprs` lit un fichier texte contenant des représentations
d'objets dans le but de recréer ces objets. Chaque ligne du fichier doit être
une représentation d'objet. Les lignes vides sont ignorées. Chaque itération
de ce générateur produit un objet.

Pour plus d'informations, consultez la documentation des fonctions et les démos
dans le dépôt de code source.

### Importation de classes et modification de `sys.path`

Recréer des objets requiert d'importer leur classe sauf s'ils sont d'un type
natif (*built-in*). À cette fin, il faut fournir à `read_reprs` les
instructions d'importation nécessaires en chaînes de caractères.

Le module ou paquet des classes importées doit être importable. C'est le cas
des paquets standards et installés. Pour les classes provenant d'autres
sources, il faut inclure le chemin du dossier parent de leur module ou paquet
dans la liste `sys.path`. Si des chemins sont fournis au générateur
`read_reprs`, il les ajoute à `sys.path`, effectue les importations puis enlève
les chemins ajoutés de `sys.path`. Si l'utilisateur modifie lui-même
`sys.path`, il ne devrait pas fournir de chemins à `read_reprs`.

Cependant, si un module ou paquet a été importé avant l'exécution de
`read_reprs`, inclure son chemin parent dans `sys.path` n'est pas nécessaire.
Le dictionnaire `sys.modules` conserve les modules et paquets importés pour
réutilisation, ce qui les rend importables dans tous les modules. Soyez prudent
en profitant de cette fonctionnalité. Autrement, `read_reprs` risque de lever
une exception `ModuleNotFoundError`.

La bibliothèque `syspathmodif`, une dépendance de `repr_rw`, offre la fonction
`sm_contains`, qui indique si `sys.modules` contient le module ou paquet dont
le nom est donné en argument. Si `sm_contains` renvoie vrai (`True`) pour un
module ou un paquet, on peut l'importer sans ajouter son chemin parent à
`sys.path`.

### Dépendances

Installez les dépendances avec cette commande.
```
pip install -r requirements.txt
```

### Démos

Le script `demo_write.py` montre comment utiliser la fonction `write_reprs`. Il
faut l'exécuter en premier, car il produit un fichier dont les démos de lecture
ont besoin.

```
python demos/demo_write.py
```

Le script `demo_read.py` montre comment utiliser la fonction `read_reprs`. Il
faut l'exécuter après `demo_write.py`, car il ne fonctionne pas sans le fichier
produit par cet autre script.

```
python demos/demo_read.py
```

Le script `demo_read_no_paths.py` montre comment la fonction `read_reprs` peut
fonctionner sans ajouter de chemins à `sys.path`. Ce script aussi a besoin du
fichier produit par `demo_write.py`.

```
python demos/demo_read_no_paths.py
```

## ENGLISH

This library writes object representations in a text file and reads the file to
recreate the objects. An object representation is a string returned by function
`repr`.

### Content

Function `write_reprs` writes object representations in a text file. Each line
in the file is an object representation. If the specified file already exists,
this function overwrites it.

Generator `read_reprs` reads a text file that contains object representations
to recreate the objects. Each line in the file must be an object
representation. Empty lines are ignored. Each iteration of this generator
yields one object.

For more information, consult the functions' documentation and the demos in the
source code repository.

### Importing classes and modifying `sys.path`

Recreating objects requires to import their class unless they are of a built-in
type. For this purpose, the user must provide the necessary import statements
to `read_reprs` as character strings.

The imported classes' module or package must be importable. It is the case for
standard and installed packages. For classes from other sources, the path to
their module's or package's parent directory must be included in list
`sys.path`. If paths are provided to generator `read_reprs`, it adds them to
`sys.path`, performs the imports and removes the added paths from `sys.path`.
If, instead, you modify `sys.path` yourself, you should not provide paths to
`read_reprs`.

However, if a module or package has been imported before `read_reprs` is
executed, including its parent path in `sys.path` is not required. Dictionary
`sys.modules` stores imported modules and packages for reuse, which makes them
importable in all modules. Be careful when benefitting from this feature.
Otherwise, `read_reprs` may raise a `ModuleNotFoundError`.

Library `syspathmodif`, a dependency of `repr_rw`, offers function
`sm_contains`, which indicates whether `sys.modules` contains the module or
package whose name is given as argument. If `sm_contains` returns `True` for a
module or package, you can import it without adding its parent path to
`sys.path`.

### Dependencies

Install the dependencies with this command.
```
pip install -r requirements.txt
```

### Demos

Script `demo_write.py` shows how to use function `write_reprs`. It must be
executed first because it makes a file that the reading demos need.

```
python demos/demo_write.py
```

Script `demo_read.py` shows how to use function `read_reprs`. It must be
executed after `demo_write.py` because it cannot work without the file made by
that other script.

```
python demos/demo_read.py
```

Script `demo_read_no_paths.py` shows how function `read_reprs` can work without
adding paths to `sys.path`. This script too needs the file made by `demo_read.py`.

```
python demos/demo_read_no_paths.py
```
