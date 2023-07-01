import datetime
import json
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import requests
import time


def get_data():
    filepath = Path(__file__).parent / "data.csv"

    if not filepath.exists():
        crawl()

    return load_data(filepath)


def load_data(filepath):
    data =  pd.read_csv(filepath, index_col=0)

    websites = {}

    for item in data.itertuples(index=False):
        url = item[4]

        if not url.startswith("https://"):
            url = "https://" + url

        websites[url] = item

    result = []

    for k,v in websites.items():
        obj = dict(url=k, title=v[1], info=v[2])
        result.append(obj)

    return result


def latest_articles():
    data = get_data()

    filepath = Path(__file__).parent / "feeds"

    feed = []
    format = "%a, %d %b %Y %H:%M:%S %Z"
    now = datetime.datetime.now()

    for website in data:
        my_feed = []

        feed_url = website['url'] + "/feed.rss"

        with open(filepath / website['url'][8:].replace("/", ".")) as fp:
            content = fp.read()

        soup = BeautifulSoup(content, "xml")

        image_url = soup.find('channel').find('image').find('url').text

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

            my_feed.append(dict(title=title, img=image_url, date=date, description=description, link=link))

        my_feed.sort(key=lambda item: item['date'], reverse=True)
        feed.extend(my_feed[:3])

    feed.sort(key=lambda d: d['date'], reverse=True)

    for item in feed:
        item['date'] = item['date'].strftime(format)

    return feed


def crawl():
    print("Downloading registry...")

    filepath = Path(__file__).parent / "data.csv"

    data = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vS6a7T0Lj4RctsmgCT-CJFKa_wMPe9Q7W_GxF9TmVqyfVDmXpZFmUh32LzMQV57C_ZbPDS6twBi2KbZ/pub?gid=138299737&single=true&output=csv',
        # Set first column as rownames in data frame
        index_col=0,
        # Parse column values to datetime
        parse_dates=['Timestamp']
    ).fillna("")

    with open(filepath, "w") as fp:
        data.to_csv(fp)

    data = load_data(filepath)

    filepath = Path(__file__).parent / "feeds"

    print("Downloading feeds...")

    for website in data:
        feed_url = website['url'] + "/feed.rss"
        print("-", feed_url)
        response = requests.get(feed_url)

        with open(filepath / website['url'][8:].replace("/", "."), "w") as fp:
            fp.write(response.text)


if __name__ == "__main__":
    import sys
    import time

    timeout = int(sys.argv[1])

    while True:
        crawl()
        time.sleep(timeout)
