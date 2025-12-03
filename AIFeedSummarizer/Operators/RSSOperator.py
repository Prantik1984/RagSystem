import feedparser

class RssOperator:
    def __init__(self,feed_url:str):
        self.feed_url = feed_url

    def get_feed_details(self):
        """
            Downloads and parses the RSS feed.
            Returns a list of articles with title + link + summary.
        """

        feed = feedparser.parse(self.feed_url)

        if feed.bozo:
            print("Error reading RSS feed:", feed.bozo_exception)
            return None

        articles = []
        for entry in feed.entries:
            articles.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "summary": entry.get("summary", ""),
                "published": entry.get("published", ""),
            })

        print(articles)
