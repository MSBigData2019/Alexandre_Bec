from bs4 import BeautifulSoup
import re
import requests
import pandas as pd

'''
Scraping following infos on reuters.com Financial reports

* Sales for Quarter 4
* Share Price and % evolution at the time of crawling
* % Shares Owned by institutionnal investors
* Company, Sector & Industry dividend yield
'''


def url_to_soup(link):
    result = requests.get(link)
    if result.status_code == 200:
        html_doc = result.text
        soup = BeautifulSoup(html_doc, "html.parser")
        return soup
    else:
        print("Request Error")


def string_op2(string):
    char_list = ["\t", "\n", "\r", " ", "(", ")"]
    return re.sub("|".join(char_list), "", string)


def get_company_report(soup, company):
    quarter_sales = soup.find(class_="stripe").text.split("\n")[3]
    share_price = string_op2(soup.find("div", class_="sectionQuote nasdaqChange").findAll("span")[1].text)
    price_change = string_op2(
        soup.find("div", class_="sectionQuote priceChange").find(class_="valueContentPercent").text)[1:-1]
    company_div_yield = soup.find("td", text="Dividend Yield").parent.text.split("\n")[2]
    sector_div_yield = soup.find("td", text="Dividend Yield").parent.text.split("\n")[3]
    industry_div_yield = soup.find("td", text="Dividend Yield").parent.text.split("\n")[4]
    shares_owned = soup.find("td", text="% Shares Owned:").parent.text.split("\n")[2:3]
    return {"Cmpany": company,
            "Quart.Sales": quarter_sales,
            "Crt.Shar.Price": share_price,
            "Shar.Price.Var": price_change,
            "Compny.DivYld": company_div_yield,
            "Sector.DivYld": sector_div_yield,
            "IndustryDivYld": industry_div_yield,
            "Inst.Shares": shares_owned[0]}


def main():
    root_link = "https://www.reuters.com/finance/stocks/financial-highlights/"
    companies = {"Airbus": "AIR", "Danone": "DANO", "EDF": "EDF", "LVMH": "LVMH"}
    report_df = pd.DataFrame()

    for value in companies.values():
        temp_url = root_link + value + ".PA"
        temp_soup = url_to_soup(temp_url)
        new_df = get_company_report(temp_soup, value)
        report_df = report_df.append(new_df, ignore_index=True)

    print(report_df)


if __name__ == "__main__":
    main()
