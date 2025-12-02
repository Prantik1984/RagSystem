import os
from dotenv import load_dotenv
def Main():
    load_dotenv()
    rss_feeds=os.getenv("RSS_FEEDS")
    print(rss_feeds)

if __name__ == "__main__":
    Main()