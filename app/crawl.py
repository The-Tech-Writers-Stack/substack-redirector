import datetime
import json
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import requests
import time


def get_data(ttl=600):
    data = download_data(ttl=ttl)

    websites = {}

    for item in data.itertuples(index=False):
        url = item[4]

        if not url.startswith("https://"):
            url = "https://" + url

        websites[url] = item

    result = []

    for k,v in websites.items():
        obj = dict(url=k, title=v[1], info=v[2], )
        obj['feed'] = v[5] or k + "/feed"
        result.append(obj)

    return result


def download_data(ttl=600):
    filepath = Path(__file__).parent / "data.csv"

    if filepath.exists() and time.time() - filepath.stat().st_mtime < ttl:
        return pd.read_csv(filepath, index_col=0)

    print("Downloading registry...")

    data = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vS6a7T0Lj4RctsmgCT-CJFKa_wMPe9Q7W_GxF9TmVqyfVDmXpZFmUh32LzMQV57C_ZbPDS6twBi2KbZ/pub?gid=138299737&single=true&output=csv',
        # Set first column as rownames in data frame
        index_col=0,
        # Parse column values to datetime
        parse_dates=['Timestamp']
    ).fillna("")

    with open(filepath, "w") as fp:
        data.to_csv(fp)

    return data


def crawl_feeds(ttl=3600):
    data = get_data(ttl)

    filepath = Path(__file__).parent / "feed.json"

    if filepath.exists() and time.time() - filepath.stat().st_mtime < ttl:
        with open(filepath) as fp:
            return json.load(fp)

    print("Downloading feed...")

    feed = []
    format = "%a, %d %b %Y %H:%M:%S %Z"
    now = datetime.datetime.now()

    for item in data:
        response = requests.get(item['url'] + "/feed.rss")
        soup = BeautifulSoup(response.content, "xml")

        for item in soup.find_all('item'):
            title = item.find('title').text
            date = datetime.datetime.strptime(item.find('pubDate').text, format)
            description = item.find('description').text
            link = item.find('link').text

            if (now - date).days > 7:
                continue

            if ".substack.com/p/" in link:
                name, slug = link.split(".substack.com/p/")
                name = name[8:]
                link = "./%s/%s" % (name, slug)

            feed.append(dict(title=title, date=date.strftime(format), description=description, link=link))

    feed.sort(key=lambda d: d['date'], reverse=True)

    with open(filepath, "w") as fp:
        json.dump(feed, fp, indent=2)

    return feed
