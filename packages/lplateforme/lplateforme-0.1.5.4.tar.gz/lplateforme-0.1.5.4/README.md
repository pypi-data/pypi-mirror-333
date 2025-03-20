# Guide d'utilisation rapide du package **lplateforme** pour la création d'un jeu de plateforme

## Introduction

Le package **lplateforme** permet de créer facilement des jeux de plateforme en Python. Il fournit des outils pour gérer les objets, les plateformes, les collisions et les événements dans un environnement graphique interactif.

## Installation

Avant de commencer, assurez-vous que le package **lplateforme** est installé. Si ce n'est pas le cas, installez-le via pip :

```sh
pip install lplateforme
```

## Initialisation du jeu

Le jeu commence par l'importation du package et la définition des fonctions d'événements interactifs.

```python
from lplateforme.plateforme import *
```

## Création et gestion des plateformes

Les plateformes sont définies en utilisant la classe **BoxContainer**, qui stocke les différents éléments du niveau.

```python
plateformes = BoxContainer()
# Ajout des plateformes fixes tout autour de l'écran (1260x490) pour empêcher le joueur de tomber
plateformes.ajouter_bords(1260, 420)
# Ajout des plateformes fixes
plateformes.ajouter(Box(140, 70, 350, 278))
```

On peut également ajouter des plateformes mobiles :

```python
# Ajout des plateformes mobiles
# Plateforme horizontale qui se déplace et rebondit sur les autres plateformes
plateformes.ajouter(MovableBox(800, 70, 210, 70, "assets/platbois3.png", ['stop', "bounce"], 1, 1, obstacles=plateformes))
```

## Ajout d'objets interactifs

Les objets interactifs sont définis en tant que **EventBox** :

```python
plateformes.ajouter(EventBox(15, 385, 0, 0, "cle", "assets/cle.png", saisir_cle))
plateformes.ajouter(EventBox(400, 370, 0, 0, "coffre", "assets/coffre_ferme.png", ouvrir_coffre))
```
### Création des événements

Les fonctions d'événements permettent de définir le comportement des objets lors des interactions avec le joueur. Ces fonctions doivent être placées en début de programme. Exemple :

#### Ramasser un objet et le placer dans l'inventaire du joueur

```python
def saisir_cle(player, objet):
    if player.name == "player":
        # Transférer l'objet de la plateforme à l'inventaire du joueur
        player.obstacles.transferer(objet, player.inventaire)
        # Rendre l'objet inventaire visible
        player.inventaire.visible = True
```

#### Ouvrir un coffre avec une clé

```python
def ouvrir_coffre(player, objet):
    # Vérifier si le joueur possède une clé
    if player.name == "player":
        cle = player.inventaire.find("cle")
        if cle is not None:
            # Retirer la clé de l'inventaire du joueur
            player.inventaire.retirer(cle)
            # changer l'image du coffre par une image de coffre ouvert
            objet.image = loadImage("assets/coffre_ouvert_plein.png")
            objet.y -= 20
```


## Création du joueur

Le joueur est créé à l'aide de la classe **Player** en lui attribuant une image et des plateformes pour ses interactions :

```python
p = Player(70, 0, 20, 65, "assets/marche0.png", plateformes)
```
### remplacement de l'image du joueur par une animation
```python
animation = ImageAnimee()
animation.add_images("marche","assets/marche0.png",6)
animation.add_images("idle","assets/idle0.png",6)

p = Player(70, 0, 20, 65, animation, plateformes)
```


## Boucle principale du jeu

La boucle du jeu est structurée en trois parties : **setup**, **compute**, et **draw**.

### Initialisation du décor

```python
def setup():
    createCanvas(1260, 490)
    background(loadImage("assets/img.png"))
```

### Mise à jour des mouvements

```python
def compute():
    p.scan_keys()
    p.move()
    plateformes.move()
```

### Affichage des éléments

```python
def draw():
    plateformes.draw()
    objets.draw()
    p.draw()
    title(str(mouseXY()))
```

## Lancement du jeu

Le jeu est lancé en exécutant :

```python
run(globals())
```

## Conclusion

Ce guide vous a montré comment créer un jeu de plateforme simple avec **lplateforme**. Vous pouvez enrichir votre jeu en ajoutant plus d'événements, d'objets interactifs et de mécaniques de gameplay.

# Passe en revu des classes et fonctions du package

## Classes
### Box
Classe de base pour les plateformes fixes. Elle hérite de la classe **Rect** de pygame et ajoute une méthode **draw** pour afficher l'image de la plateforme.
paramètres:
- x, y : coordonnées du coin supérieur gauche de la plateforme
- w, h : largeur et hauteur de la plateforme
- image : chemin de l'image de la plateforme (optionnel). On peut aussi utiliser une ImageAnimee.
- collision_behavior : comportement de collision de la plateforme (optionnel). Par défaut, la plateforme est solide et empêche le joueur de passer à travers. ["stop"]. On peut utiliser "stopx" pour arrêter suivant l'axe x et stopy pour arrêter suivant l'axe y.On peut aussi utiliser "bounce" pour rebondir sur la plateforme.

### MovableBox
Classe pour les plateformes mobiles. Elle hérite de la classe **Box** et ajoute des méthodes pour gérer le mouvement de la plateforme.
paramètres:
- x, y : coordonnées du coin supérieur gauche de la plateforme
- w, h : largeur et hauteur de la plateforme
- image : chemin de l'image de la plateforme (optionnel). On peut aussi utiliser une ImageAnimee.
- collision_behavior : comportement de collision de la plateforme (optionnel). Par défaut, la plateforme est solide et empêche le joueur de passer à travers. ["stop"]. On peut utiliser "stopx" pour arrêter suivant l'axe x et stopy pour arrêter suivant l'axe y.On peut aussi utiliser "bounce" pour rebondir sur la plateforme.
- velocity_x : vitesse de déplacement suivant l'axe x
- velocity_y : vitesse de déplacement suivant l'axe y
- obstacles : liste des plateformes fixes pour gérer les collisions

### EventBox
Classe pour les objets interactifs. Elle hérite de la classe **Box** et ajoute une méthode **event** pour déclencher un événement lorsqu'un joueur entre en collision avec l'objet.
paramètres:
- x, y : coordonnées du coin supérieur gauche de l'objet
- w, h : largeur et hauteur de l'objet
- name : nom de l'objet
- image : chemin de l'image de l'objet (optionnel). On peut aussi utiliser une ImageAnimee.
- event : fonction d'événement à déclencher

### MovableGravityBox
Classe pour les plateformes mobiles avec gravité. Elle hérite de la classe **MovableBox** et ajoute un attribut **gravity** pour gérer la gravité de la plateforme.
