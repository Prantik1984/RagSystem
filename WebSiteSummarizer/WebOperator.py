from newspaper import Article
class WebOperator:

    def download_article(self, url):
        """"
        Download article from url
        """
        try:
            article = Article(url)
            article.download()
            article.parse()
            return article
        except Exception as e:
            print(e)
            return None

