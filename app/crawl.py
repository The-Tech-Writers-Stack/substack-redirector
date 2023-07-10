import datetime
import json
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import requests
import time
import shelve


def get_data():
    filepath = Path(__file__).parent / "data.csv"

    if not filepath.exists():
        crawl()

    return load_data(filepath)


def load_data(filepath):
    data = pd.read_csv(filepath, index_col=0, parse_dates=["Timestamp"])

    websites = {}

    for item in data.itertuples(index=True):
        url = item[5]

        if not url.startswith("https://"):
            url = "https://" + url

        if url.endswith(".substack.com"):
            url = f"https://techwriters.info/{url[8:-13]}"

        websites[url] = item

    result = []

    db = shelve.open("clicks.db", flag="c")

    for url, row in websites.items():
        image_url = url + "/favicon.ico"
        clicks = 0

        if url.startswith("https://techwriters.info/"):
            substack = url[25:]
            image_url = f"https://{substack}.substack.com/favicon.ico"
            clicks = db.get(substack, 0)

        topics = row[12]

        if isinstance(topics, str):
            topics = topics.replace(",", ";")

            if "Literature; art; and media" in topics:
                topics = topics.replace("Literature; art; and media", "Literature, art, and media")

            topics = [s.strip() for s in topics.split(";")]
        else:
            topics = []

        obj = dict(
            url=url,
            title=row[2].strip(),
            info=row[3].strip(),
            date=row[0],
            image_url=image_url,
            topics=topics,
            clicks=clicks
        )
        result.append(obj)

    return result


def latest_articles(max_per_author=0, max_words=0):
    data = get_data()

    filepath = Path(__file__).parent / "feeds"

    feed = []
    format = "%a, %d %b %Y %H:%M:%S %Z"
    now = datetime.datetime.now()

    for website in data:
        my_feed = []

        with open(filepath / website["url"][8:].replace("/", ".")) as fp:
            content = fp.read()

        soup = BeautifulSoup(content, "xml")

        try:
            image_url = soup.find("channel").find("image").find("url").text

            for item in soup.find_all("item"):
                title = item.find("title").text
                date = datetime.datetime.strptime(item.find("pubDate").text, format)
                description = item.find("description").text
                link = item.find("link").text

                if max_words > 0:
                    description = description.split()

                    if len(description) > max_words:
                        description = " ".join(description[:max_words]) + "..."
                    else:
                        description = " ".join(description)

                if (now - date).days > 7:
                    continue

                if ".substack.com/p/" in link:
                    name, slug = link.split(".substack.com/p/")
                    name = name[8:]
                    link = "./%s/%s" % (name, slug)

                my_feed.append(
                    dict(
                        title=title.strip(),
                        author=website["title"],
                        url=website["url"],
                        img=image_url,
                        date=date,
                        description=description.strip(),
                        link=link,
                    )
                )

        except AttributeError:
            continue

        my_feed.sort(key=lambda item: item["date"], reverse=True)

        if max_per_author > 0:
            my_feed = my_feed[:max_per_author]

        feed.extend(my_feed)

    feed.sort(key=lambda d: d["date"], reverse=True)

    for item in feed:
        item["date"] = item["date"].strftime(format)

    return feed


def new_members(data):
    today = datetime.datetime.today()
    return [w for w in data if (today - w["date"]).days <= 7]


def crawl():
    print("Downloading registry...")

    filepath = Path(__file__).parent / "data.csv"

    data = pd.read_csv(
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vS6a7T0Lj4RctsmgCT-CJFKa_wMPe9Q7W_GxF9TmVqyfVDmXpZFmUh32LzMQV57C_ZbPDS6twBi2KbZ/pub?gid=138299737&single=true&output=csv",
        # Set first column as rownames in data frame
        index_col=0,
        # Parse column values to datetime
        parse_dates=["Timestamp"],
    ).fillna("")

    with open(filepath, "w") as fp:
        data.to_csv(fp)

    data = load_data(filepath)

    filepath = Path(__file__).parent / "feeds"

    print("Downloading feeds...")

    for website in data:
        feed_url = website["url"] + "/feed.rss"

        if feed_url.startswith("https://techwriters.info/"):
            substack = feed_url[25:-9]
            feed_url = f"http://{substack}.substack.com/feed.rss"

        print("-", feed_url)
        response = requests.get(feed_url, allow_redirects=True)

        with open(filepath / website["url"][8:].replace("/", "."), "w") as fp:
            fp.write(response.text)


if __name__ == "__main__":
    import sys
    import time

    timeout = int(sys.argv[1])

    while True:
        crawl()

        if timeout == 0:
            break

        time.sleep(timeout)
