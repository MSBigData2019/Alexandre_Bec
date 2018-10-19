# Github API top users stars repo

from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

'''
- Récupérer via crawling la liste des 256 top contributors sur cette page https://gist.github.com/paulmillr/2657075
- En utilisant l'API github https://developer.github.com/v3/
- Récupérer pour chacun de ces users
    le nombre moyens de stars des repositories qui leur appartiennent.
- Pour finir classer ces 256 contributors par leur note moyenne.﻿
'''


def url_to_soup(link):
    result = requests.get(link)
    if result.status_code == 200:
        html_doc = result.text
        soup = BeautifulSoup(html_doc, "html.parser")
        return soup
    else:
        print("Request Error")


def get_top_contribs_names_list(url):
    soup = url_to_soup(url)
    table = soup.find(lambda tag: tag.name == 'tbody')
    rows = list()
    for row in table.findAll("tr"):
        rows.append(row.text)
    return(rows)


def get_links_list(url):
    soup = url_to_soup(url)

    rank_list = []
    profile_link_list = []
    pseudo_list = []
    name_list = []

    for link in soup.table.tbody.findAll("tr"):

        rank_list.append(link.find("th").text.strip("#"))
        profile_link_list.append(link.find("td").find("a").get("href"))
        pseudo_list.append(link.find("td").text.split(" ")[0])
        name_list.append("".join(link.find("td").text.split(" ")[1:]).strip("(").strip(")"))

    git_top_df = pd.DataFrame({'ranking': rank_list, 'pseudo': pseudo_list, 'profile_link': profile_link_list, 'name': name_list})\
        .set_index('ranking')

    return git_top_df

def get_user_starsum(user):
    username = "alexpeterbec"
    token = open(".API_KEY", 'r').read()
    base_link = "https://api.github.com/users/"+user+"/repos"

    # Get number of pages
    req_page = requests.get(base_link, auth=(username, token))

    if not req_page.links:
        pages_repo = 1
    else:
        pages_repo = req_page.links["last"]["url"].split("=")[1]

    print(pages_repo)

    ''' ITERATE ON PAGES '''

    sum_stars = 0
    sum_repos = 0

    for page_nb in range(0,int(pages_repo)):
        repos_group = requests.get(base_link + "?page=" + str(page_nb), auth=(username, token))

        # Raw text for repo @ page_nb
        page_json = json.loads(repos_group.content)
        sum_repos += len(page_json)

        for j in range(len(page_json)):
            sum_stars += page_json[j].get("stargazers_count")

    return (sum_stars, sum_repos)


def main():
    root_link = "https://gist.github.com/paulmillr/2657075"
    users_list = get_top_contribs_names_list(root_link)

    git_df = get_links_list(root_link)
    #print(git_df)

    print(get_user_starsum("alexpeterbec"))


if __name__ == "__main__":
    main()