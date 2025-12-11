import os
from dotenv import load_dotenv
from Operators.RSSOperator import RssOperator
from Operators.DbOperator import DbOperator
import json
import sys

operation_type=None
query_string=None

def read_args():
    """"
    reads the command line arguments
    """
    global operation_type
    global query_string
    for arg in sys.argv:
        if(arg=='--f'):
            operation_type="Retrieve_Feeds"

        if (arg == '--s'):
            operation_type = "Query_Feeds"

        if(arg.startswith('--q')):
            query_string=arg[3:]

def Main():
    load_dotenv()
    read_args()
    match operation_type:
      case "Retrieve_Feeds":
          retrieve_feeds()
      case "Query_Feeds":
          if query_string is None:
              print("No query string provided")
              return
          run_query(query_string)


def run_query(query):
    db_operator=DbOperator()
    db_operator.QueryDb(query)

def retrieve_feeds():
    rss_feeds_raw=os.getenv("RSS_FEEDS")
    rss_feeds=json.loads(rss_feeds_raw)
    rss_articles=[]
    for feed in rss_feeds:
        rss_operator=RssOperator(feed)
        articles=rss_operator.get_feed_details()
        if articles != None:
            rss_articles.extend(articles)
    if len(rss_articles)>0:
        db_operator=DbOperator()
        db_operator.index_rss_items(rss_articles)
    with open("output.json", "w") as f:
        json.dump(rss_articles, f, indent=4)

if __name__ == "__main__":
    Main()