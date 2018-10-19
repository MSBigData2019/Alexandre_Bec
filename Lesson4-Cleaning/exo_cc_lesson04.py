# API Distance Matrix

from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

'''
Créer une matrice de distances entre les 50 plus grandes villes francaises.﻿


Ameliorations :
- Paralleliser les traitements
- Mise en forme output : dataframe / csv / 2D Array
- Passer sur l'API Google
'''


def url_to_soup(link):
    result = requests.get(link)
    if result.status_code == 200:
        html_doc = result.text
        soup = BeautifulSoup(html_doc, "html.parser")
        return soup
    else:
        print("Request Error")


def create_list_cities(file):
    cities_file = open(file, 'r').readlines()
    list_cities = []
    for line in cities_file:
        list_cities.append(line.split('\t')[1])

    return list_cities


def read_cities_xls(file):
    pop_xls = pd.read_excel(file, skiprows=7, sheetname="Communes")


def api_distance(source, destination):
    url = "https://fr.distance24.org/route.json?stops="+source+"|"+destination
    response = requests.get(url)
    distance = json.loads(response.content).get('distance')
    return distance


def main():
    cities = create_list_cities("data/cities.txt")

    print(api_distance("Paris", "Marseille"))

    for i in range(0,len(cities)):
        for j in range(i+1,len(cities)):
            print(cities[i], " - ", cities[j], " : ", api_distance(cities[i], cities[j]))


if __name__ == "__main__":
    main()