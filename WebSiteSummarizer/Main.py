from langchain_community.chat_models import ChatOllama
from WebOperator import WebOperator

def Main():
    site_link="https://www.artificialintelligence-news.com/news/alibaba-qwen-ai-app-10-million-downloads/"
    webOperator = WebOperator()
    article=webOperator.download_article(site_link)
    print(article)

if __name__ == "__main__":
    Main()