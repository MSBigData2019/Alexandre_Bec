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


def ads_number(soup):
    nb_ads = soup.find(class_="numAnn").text
    return int(nb_ads)


def get_ad_info(soup):
    ref = "https://www.lacentrale.fr" + soup.a.get('href')
    version = soup.find(class_='brandModelTitle').text[11:]
    year = int(soup.find("div", class_='fieldYear').text)
    mileage = int(soup.find("div", class_='fieldMileage').text.replace("\xa0", "").replace("km", ""))
    price = int(soup.find(class_='fieldPrice').text.replace("\xa0", "").replace("€", ""))
    seller = str(soup.find(class_='typeSellerGaranty').text.split(" ")[0])

    return ref, version, year, mileage, price, seller


def get_phone(url):
    soup = url_to_soup(url)
    phone_raw = soup.find(class_="phoneNumber1").text.replace("\xa0", "")

    return str(re.compile('\d{10}').findall(phone_raw)[0])


def scrap_page(soup):

    table = soup.find(class_="resultListContainer").find_all(class_="adLineContainer")
    ads_treated = 0
    ref_link, version, year, mileage, price, seller, phone = "", "", int(), int(), int(), "", ""

    for adLineContainer in table:

        if adLineContainer.find(class_="adContainer") is None: continue
        adContainer = adLineContainer.find(class_="adContainer")

        #[ref_link, version, year, mileage, price, seller]
        ref_link, version, year, mileage, price, seller = get_ad_info(adContainer)
        phone = get_phone(ref_link)
        ads_treated += 1
        print(ref_link, version, year, mileage, price, seller, phone)

    return ads_treated, ref_link, version, year, mileage, price, seller, phone


def iterate_pages(ads_nb):

    break_loop = False
    page = 1
    treated = 0

    while not break_loop:
        print("Scraping page "+str(page))
        url = "https://www.lacentrale.fr/listing?makesModelsCommercialNames=RENAULT%3AZOE&options=&page="+str(page)+"&r" \
              "egions=FR-PAC%2CFR-IDF%2CFR-NAQ"
        soup = url_to_soup(url)
        treated += scrap_page(soup)[0]
        page += 1

        if treated == ads_nb:
            break_loop = True

    return


def main():
    url = "https://www.lacentrale.fr/listing?makesModelsCommercialNames=RENAULT%3AZOE&options=&page=2&regions=" \
          "FR-PAC%2CFR-IDF%2CFR-NAQ"
    soup = url_to_soup(url)
    #test_page()
    iterate_pages(ads_number(soup))
    #scrap_page(soup)



if __name__ == "__main__":
        main()



