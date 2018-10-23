'''
Générer un fichier de données sur le prix des Renault Zoé sur le marché de l'occasion en Ile de France, PACA et Aquitaine.
Vous utiliserez lacentrale, paruvendu, autoplus,...
Le fichier doit être propre et contenir les infos suivantes :
    - version (il y en a 3),
    - année, kilométrage,
    - prix,
    - téléphone du propriétaire,
    - est ce que la voiture est vendue par un professionnel ou un particulier.

    - ajouter une colonne sur le prix de l'Argus du modèle que vous récupérez sur ce site
    http://www.lacentrale.fr/cote-voitures-renault-zoe--2013-.html.

Les données quanti (prix, km notamment) devront être manipulables (pas de string, pas d'unité).
Vous ajouterez une colonne si la voiture est plus chere ou moins chere que sa cote moyenne.﻿
'''

import requests

