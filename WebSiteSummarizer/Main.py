from langchain_community.chat_models import ChatOllama
from WebOperator import WebOperator
from ..QuerringTextFiles.Embedder import Embedder
from Chunker import Chunker
def Main():
    site_link="https://www.artificialintelligence-news.com/news/alibaba-qwen-ai-app-10-million-downloads/"
    webOperator = WebOperator()
    article=webOperator.download_article(site_link)

    chunk_creator= Chunker()
    chunked_texts= chunk_creator.chunk_text(article)
    print(chunked_texts)
if __name__ == "__main__":
    Main()