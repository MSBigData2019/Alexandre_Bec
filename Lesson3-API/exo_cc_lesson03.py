# Discount Scraping RDC

from bs4 import BeautifulSoup
import re
import requests

def url_to_soup(link):
    result = requests.get(link)
    if result.status_code == 200:
        html_doc = result.text
        soup = BeautifulSoup(html_doc, "html.parser")
        return soup
    else:
        print("Request Error")


def get_nb_results(soup):
    return soup.find("div", class_="list_number_product").find().text.split(" ")[0]


def get_nb_discount(soup):
    # Nombre de remise sur page 1
    try:
        remises = soup.find('p', class_='darty_prix_barre_remise darty_small separator_top').text
    except:
        print("Pas de remise, c'est Apple")
    print(remises)


def main():
    root_link = "https://www.darty.com/nav/recherche?s=relevence&text="
    brands = ["dell", "acer", "asus", "apple"]
    trail_link = "&fa=756"

    for brand in brands:
        link = root_link + brand + trail_link
        soup = url_to_soup(link)
        print(link)
        print("Nombre de produits trouvés : ", get_nb_results(soup))
        get_nb_discount(soup)



if __name__ == "__main__":
    main()
