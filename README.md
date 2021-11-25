# Jeu-de-Go

**Date de réalisation :** Décembre 2019

**Cadre du projet :** Cours "HCI and GUI Programming" à Griffith College en Faculté d’informatique durant mon semestre académique à Dublin, réalisé en binôme avec Katell

**Langage utilisé :** Python

Le jeu de Go (jeu d’encerclement) a été inventé en Chine il y a plus de 3000 ans.
Il s’agit d’un jeu stratégique à deux joueurs dont le but est d’occuper plus de territoire que l’adversaire.  Chacun leur tour, les joueurs placent des pierres noires ou blanches sur un plateau quadrillé appelé goban. Les pierres encerclées par les pierres adverses deviennent des prisonniers.

J’ai créé une interface graphique permettant de jouer à ce jeu, en utilisant une grille plus petite que ce qui est normalement utilisé afin de permettre des parties plus rapides (grille 7x7 au lieu de 13x13 ou 19x19).

Le joueur qui commence possède les pierres noires. Il peut les placer à n’importe quelle intersection de la grille inoccupée à condition de respecter ces 2 règles :

-	Règle du suicide : on ne peut pas placer une pierre de telle manière qu’après le coup elle n’ait plus aucune liberté.

-	Règle du KO : pour éviter qu'une situation ne se répète à l'infini, la règle du KO interdit de jouer un coup qui ramènerait le jeu dans une position déjà vue dans le courant de la partie.
