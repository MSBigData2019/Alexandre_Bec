# Crawling de données
import requests
import unittest
from bs4 import BeautifulSoup

# TODO : Request Builder (price range, keywords, location, categories..)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def build_soup_object(url):
    r = requests.get(url, headers=headers)
    soup = None
    if (r.status_code == 200): # Status code = INT
        soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def beautifulsoup_basics(url):
    r = requests.get(url, headers=headers)
    print(r.status_code)
    print(r.content)

    soup = build_soup_object(url)
    print("\n\nHead of HTML file :\n" + soup.prettify()[0:1000])
    print("\n\nChildren list :\n" + str(list(soup.children))[0:1000]+"\n\n")

    for item in list(soup.children):
        print(type(item))

    html = list(soup.children)[2]
    print("\n"+str(type(html)))
    print("\n\nTag exploration :\n" + str(list(html.children))[0:1000] + "\n\n")

    body = list(html.children)[3]
    p = list(body.children)[1]
    print(p.get_text())

def find_instances(url):
    soup = build_soup_object(url)
    paragraphs = soup.find_all('p')[0].get_text()
    print(paragraphs)

    # First only
    paragraphs = soup.find('p').get_text()
    print(paragraphs)

def advanced_search(url):
    soup = build_soup_object(url)
    print("\n", soup)

    print("\n\n"+"Filter on tag, class name")
    filteredParagraphClass = soup.find_all("p", class_="outer-text")
    print(filteredParagraphClass)

    print("\n\n"+"Filter on ID")
    filteredID = soup.find_all(id="first")
    print(filteredID)

    print("\n\n"+"Filter with CSS style : div p")
    # Les P à l'interieur d'une balise div
    filteredCSS = soup.select("div p")
    print(filteredCSS)
    return


def main():
    #unittest.main()
    simple_page = "http://dataquestio.github.io/web-scraping-pages/simple.html"
    find_instances(simple_page)

    complete_page = "http://dataquestio.github.io/web-scraping-pages/ids_and_classes.html"
    advanced_search(complete_page)


if __name__ == '__main__':
    main()