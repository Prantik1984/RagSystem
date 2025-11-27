from langchain_community.chat_models import ChatOllama
from WebOperator import WebOperator
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from QuerringTextFiles.Embedder import Embedder
from Chunker import Chunker
def Main():
    site_link="https://www.artificialintelligence-news.com/news/alibaba-qwen-ai-app-10-million-downloads/"
    webOperator = WebOperator()
    article=webOperator.download_article(site_link)

    chunk_creator= Chunker()
    chunked_texts= chunk_creator.chunk_text(article)

    embedder = Embedder()
    vector = embedder.get_embeddings(chunked_texts)
    retriever = vector.as_retriever(search_kwargs={"k": 2})
if __name__ == "__main__":
    Main()