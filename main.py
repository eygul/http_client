import requests
from bs4 import BeautifulSoup
import re
import json


def scrape_website(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    raw = soup.pre.text
    pattern = re.compile(
        r'\d{4}\.\d{2}\.\d{2}\s+\d{2}:\d{2}:\d{2}\s+[\d.]+\s+[\d.]+\s+[\d.]+\s+-.-\s+['
        r'\d.]+\s+-.-\s+\S+(?:\s\S+)*?\s'
    )
    matches = pattern.findall(raw)
    scrape_matches = []
    for match in matches:
        lst = match.split()
        scrape_matches.append(lst)
    print(scrape_matches)
    return scrape_matches


def api_scrape(url):
    database = []
    req = requests.get(url)
    res = req.text
    jquake = json.loads(res)
    for quake in jquake:
        api_list = list(quake.values())
        api_list.pop(0)
        database.append(api_list)
    print(database)
    return database


def post():
    auth_token = 'your auth token'
    headers = {'Authorization': f'Token {auth_token}'}
    url = 'your url'
    scrape_matches = scrape_website("your url")
    database = api_scrape("your url")
    for scrape in scrape_matches:
        if scrape not in database:
            date = scrape[0]
            time = scrape[1]
            latitude = scrape[2]
            longitude = scrape[3]
            depth = scrape[4]
            md = scrape[5]
            ml = scrape[6]
            mw = scrape[7]
            location = scrape[8]
            data = {'date': date,
                    'time': time,
                    'latitude': latitude,
                    'longitude': longitude,
                    'depth': depth,
                    'md': md,
                    'ml': ml,
                    'mw': mw,
                    'location': location}
            response = requests.post(url, json=data, headers=headers)
            print(response)
            print(response.json())


post()
