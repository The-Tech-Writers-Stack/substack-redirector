from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import time
import jinja2


def get_data():
    data = download_data()

    websites = {}

    for item in data.itertuples(index=False):
        url = item[4]

        if not url.startswith("https://"):
            url = "https://" + url

        websites[url] = item

    return [dict(url=k, title=v[1], info=v[2]) for k,v in websites.items()]


def download_data():
    filepath = Path(__file__).parent / "data.csv"

    if not filepath.exists() or time.time() - filepath.stat().st_mtime > 300:
        print("Downloading...")

        data = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vS6a7T0Lj4RctsmgCT-CJFKa_wMPe9Q7W_GxF9TmVqyfVDmXpZFmUh32LzMQV57C_ZbPDS6twBi2KbZ/pub?gid=138299737&single=true&output=csv',
                        # Set first column as rownames in data frame
                        index_col=0,
                        # Parse column values to datetime
                        parse_dates=['Timestamp']
                        )

        with open(filepath, "w") as fp:
            data.to_csv(fp)

    return pd.read_csv(filepath, index_col=0)
