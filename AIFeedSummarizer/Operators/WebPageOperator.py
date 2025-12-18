import trafilatura

class WebPageOperator:
    def __init__(self):
        pass

    def get_webpage_text(self,url:str)-> str:
        """"
        download the webpage text from the url
        """
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            return {"result":False}

        text = trafilatura.extract(downloaded, include_comments=False, include_tables=False)
        return {"result":True,"content":text}