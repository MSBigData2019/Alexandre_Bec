'''
Générer un fichier de données sur le prix des Renault Zoé sur le marché de l'occasion en Ile de France, PACA et Aquitaine.
Vous utiliserez lacentrale, paruvendu, autoplus,...
Le fichier doit être propre et contenir les infos suivantes :
    - Version (il y en a 3),
    - Année, kilométrage,
    - Prix
    - est ce que la voiture est vendue par un professionnel ou un particulier.

    - ajouter une colonne sur le prix de l'Argus du modèle que vous récupérez sur ce site
    http://www.lacentrale.fr/cote-voitures-renault-zoe--2013-.html.

Les données quanti (prix, km notamment) devront être manipulables (pas de string, pas d'unité).
Vous ajouterez une colonne si la voiture est plus chere ou moins chere que sa cote moyenne.﻿
'''

import requests
import re
from bs4 import BeautifulSoup


def url_to_soup(link):
    result = requests.get(link)
    if result.status_code == 200:
        html_doc = result.text
        soup = BeautifulSoup(html_doc, "html.parser")
        return soup
    else:
        print("Request Error")


def scrap_page(link):
    soup = url_to_soup(link)
    table = soup.find_all("div", class_='adLineContainer')

    for adLineContainer in table:
        print(adLineContainer)

        ref = "https://www.lacentrale.fr"+adLineContainer.a.get('href')
        print("RefLien : " + ref)

        version = adLineContainer.find(class_='brandModelTitle').text[11:]
        print("Model : "+version)

        year = adLineContainer.find("div", class_='fieldYear').text
        print("Year : " + year)

        mileage = int(adLineContainer.find("div", class_='fieldMileage').text\
            .replace("\xa0", "")\
            .replace("km", ""))
        print("Mileage : " + str(mileage))

        prix = int(adLineContainer.find(class_='fieldPrice').text \
            .replace("\xa0", "")\
            .replace("€", ""))
        print("Prix : "+str(prix))

        seller = str(adLineContainer.find(class_='typeSellerGaranty').text.split(" ")[0])
        print("Vendeur : "+seller)


def main():
    url = "https://www.lacentrale.fr/listing?makesModelsCommercialNames=RENAULT%3AZOE&options=&page=1&regions=FR-PAC%2CFR-IDF%2CFR-NAQ"
    scrap_page(url)




if __name__ == "__main__":
        main()



