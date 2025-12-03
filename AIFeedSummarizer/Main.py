import os
from dotenv import load_dotenv
from Operators.RSSOperator import RssOperator
import json
def Main():
    load_dotenv()
    rss_feeds_raw=os.getenv("RSS_FEEDS")
    rss_feeds=json.loads(rss_feeds_raw)
    for feed in rss_feeds:
        rss_operator=RssOperator(feed)
        rss_operator.get_feed_details()


if __name__ == "__main__":
    Main()