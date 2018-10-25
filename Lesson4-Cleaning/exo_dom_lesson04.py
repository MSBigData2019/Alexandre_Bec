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
import pandas as pd


def url_to_soup(link):
    result = requests.get(link)
    if result.status_code == 200:
        html_doc = result.text
        soup = BeautifulSoup(html_doc, "html.parser")
        return soup
    else:
        print("Request Error")


def ads_number(url):
    soup = url_to_soup(url)
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


def get_argus(link):
    soup_argus = url_to_soup(link)
    return int(soup_argus.find(class_="jsRefinedQuot").text.replace(" ", ""))


def iterate_argus():
    years = [2012]
    #2013, 2014, 2015, 2016, 2017, 2018
    model_name_list = []
    year_list = []
    price_argus = []

    for year in years:
        root_link = "https://www.lacentrale.fr/cote-voitures-renault-zoe--"+str(year)+"-.html"
        model_page_soup = url_to_soup(root_link)
        model_list = model_page_soup.find(class_="listingResult").find_all(class_="listingResultLine auto sizeA")
        for resultLine in model_list:
            link = "https://www.lacentrale.fr/"+resultLine.a.get('href')
            year_list.append(year)
            price_argus.append(get_argus(link))
            model_name_list.append(resultLine.a.text.split("\n")[2])

    #print(model_name_list)
    argus_df = pd.DataFrame({'model':model_name_list, 'year':year_list, 'argus':price_argus})
    print(argus_df)
    return argus_df


def scrap_page(soup):

    table = soup.find(class_="resultListContainer").find_all(class_="adLineContainer")
    ads_treated = 0
    #ref_link, version, year, mileage, price, seller, phone = "", "", int(), int(), int(), "", ""
    ref_link_list = []
    version_list = []
    year_list = []
    mileage_list = []
    price_list = []
    seller_list = []
    phone_list = []

    for adLineContainer in table:

        if adLineContainer.find(class_="adContainer") is None:
            continue
        ad_container = adLineContainer.find(class_="adContainer")

        result = get_ad_info(ad_container)

        ads_treated += 1
        ref_link_list.append(result[0])
        version_list.append(result[1])
        year_list.append(result[2])
        mileage_list.append(result[3])
        price_list.append(result[4])
        seller_list.append(result[5])
        phone_list.append(get_phone(result[0]))

    temp_ads_df = pd.DataFrame({
        'ref_link':ref_link_list,
        'version':version_list,
        'year':year_list,
        'mileage':mileage_list,
        'price':price_list,
        'seller':seller_list,
        'phone:':phone_list})

    return ads_treated, temp_ads_df


def iterate_pages(ads_nb):

    break_loop = False
    page, treated = (1, 0)

    link, version, year, mileage, price, seller, phone = [], [], [], [], [], [], []

    ads_df = pd.DataFrame({
        'ref_link': link, 'version': version,
        'year': year, 'mileage': mileage,
        'price': price, 'seller': seller, 'phone:': phone})

    while not break_loop:
        print("Scraping page "+str(page))
        url = "https://www.lacentrale.fr/listing?makesModelsCommercialNames=RENAULT%3AZOE&options=&page="+str(page)\
               + "&regions=FR-PAC%2CFR-IDF%2CFR-NAQ"
        soup = url_to_soup(url)
        response = scrap_page(soup)

        temp_df = response[1]
        ads_df = ads_df.append(temp_df)

        page += 1
        treated += response[0]
        if treated == ads_nb:
            break_loop = True

    return ads_df


def main():
    url = "https://www.lacentrale.fr/listing?makesModelsCommercialNames=RENAULT%3AZOE&options=&page=2&regions=" \
          "FR-PAC%2CFR-IDF%2CFR-NAQ"

    print("Building Argus DataFrame...")
    argus_df = iterate_argus()

    print("Building Ads Dataframe...")
    ads_df = iterate_pages(ads_number(url))
    print(ads_df)


if __name__ == "__main__":
        main()