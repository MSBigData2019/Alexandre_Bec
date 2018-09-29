import requests
from bs4 import BeautifulSoup
import pandas as pd

# Source : https://www.dataquest.io/blog/web-scraping-tutorial-python/


def build_request_result(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko)'
        ' Chrome/39.0.2171.95 Safari/537.36'
    }
    return requests.get(url, headers=headers)


def forecast_extract():
    url = "http://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168"
    page = build_request_result(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    seven_day = soup.find(id="seven-day-forecast")
    forecast_items = seven_day.find_all(class_="tombstone-container")
    tonight = forecast_items[0]
    print(tonight.prettify())

    '''
    name = tonight.find("p").get_text()
    condition = tonight.find(class_="short-desc").get_text()
    temp = tonight.find(class_="temp").get_text()
    img = tonight.find("img")['title']
    print("\n\n", name, "\n", conditions, "\n", temp, "\n", img, "\n")
    '''

    periods = [pt.get_text() for pt in seven_day.select(".tombstone-container .period-name")]
    conditions = [cond.get_text() for cond in seven_day.select(".tombstone-container .short-desc")]
    temps = [temp.get_text() for temp in seven_day.select(".tombstone-container .temp")]
    descs = [d["title"] for d in seven_day.select(".tombstone-container img")]

    weather = pd.DataFrame({
        "Period": periods,
        "Condition": conditions,
        "Temperature": temps,
        "Description": descs
    })

    print(weather)

def main():
    forecast_extract()


if __name__ == '__main__':
    main()