# API Distance Matrix

from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

'''
Créer une matrice de distances entre les 50 grandes villes francaises.﻿
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

    return(list_cities)

def read_cities_xls(file):
    pop_xls = pd.read_excel(file, skiprows=7, sheetname="Communes")


def api_distance(source, destination):
    url = "https://fr.distance24.org/route.json?stops="+source+"|"+destination


def main():
    print(create_list_cities("cities.txt"))
    read_cities_xls("ensemble.xls")

if __name__ == "__main__":
    main()