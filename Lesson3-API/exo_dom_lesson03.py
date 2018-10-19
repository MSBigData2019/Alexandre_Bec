# Github API top users stars repo

from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import time

'''
- Récupérer via crawling la liste des 256 top contributors sur cette page https://gist.github.com/paulmillr/2657075
- En utilisant l'API github https://developer.github.com/v3/
- Récupérer pour chacun de ces users
    le nombre moyens de stars des repositories qui leur appartiennent.
- Pour finir classer ces 256 contributors par leur note moyenne.﻿

Ameliorations possibles :
- Concatenation Dataframes
- Ne pas faire la moyenne "à la main"
- Parallelisation
- Compte d'appels de l'API (variable globale ?)
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
    return rows


def build_user_data(url):
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


def get_page_number_for_user(link, username, token):

    req_page = requests.get(link, auth=(username, token))

    if not req_page.links:
        return 1
    else:
        return req_page.links["last"]["url"].split("=")[1]



def get_user_starsum(user, username, token):

    base_link = "https://api.github.com/users/"+user+"/repos"

    pages_repo = get_page_number_for_user(base_link, username, token)
    sum_stars = 0
    sum_repos = 0

    for page_nb in range(0,int(pages_repo)):
        repos_group = requests.get(base_link + "?page=" + str(page_nb), auth=(username, token))

        page_json = json.loads(repos_group.content)
        sum_repos += len(page_json)

        for j in range(len(page_json)):
            sum_stars += page_json[j].get("stargazers_count")

    return sum_repos, sum_stars


def create_star_ranking(userlist, username, token):

    mean_star_list = []
    count = 256

    for user in userlist:
        for_loop_start = time.time()
        res = get_user_starsum(user, username, token)
        if res[0] == 0:
            mean_star_list.append(int(0))
        else:
            mean_star_list.append(int(res[1] / res[0]))

        count -= 1
        for_loop_end = time.time()
        print(user, count, int(for_loop_end-for_loop_start))

    star_ranking = pd.DataFrame({"username":userlist, "mean_star":mean_star_list})
    return star_ranking


def main():

    start_time = time.time()

    USERNAME = "alexpeterbec"
    TOKEN = open(".API_KEY", 'r').read()

    root_link = "https://gist.github.com/paulmillr/2657075"
    users_list = get_top_contribs_names_list(root_link)

    git_df = build_user_data(root_link)
    #print(git_df['pseudo'])

    #print(get_user_starsum("alexpeterbec", USERNAME, TOKEN))
    rank_df = create_star_ranking(git_df['pseudo'], USERNAME, TOKEN)
    print(rank_df)

    end_time = time.time()

    rank_df.to_csv("Github Ranking.csv", "\t")

    print("Execution Time : ", (end_time-start_time)%60)


if __name__ == "__main__":
    main()