import os
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions
from .WebPageOperator import WebPageOperator
from .LLMSummarizer import LLMSummarizer

class DbOperator:
    def __init__(self):
        load_dotenv()
        self.db_name = os.getenv("DB_NAME")
        self.db_path = os.getenv("DB_PATH")
        # self.articles_db = os.getenv("ARTICLES_DB")

    def fetch_article_data(self,link:str):
        """"
        checks if the article link has been saved
        if yes returns its vector
        else downloads, saves and returns the vector
        """

        client = chromadb.PersistentClient(path=self.db_path)
        embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=os.getenv("MODEL_NAME")
        )
        collection = client.get_or_create_collection(
            name=os.getenv("ARTICLES_DB"),
            embedding_function=embedder,
            metadata={"hnsw:space": "cosine"}
        )
        results = collection.query(
            query_texts=[link],
            n_results=1,
        )
        if results["ids"] and len(results["ids"][0]) > 0:
            content = results["documents"][0][0]
            llm_summarizer = LLMSummarizer()
            summary = llm_summarizer.summarize_article(content)

        else:
            webpage_operator=WebPageOperator()
            result_text=webpage_operator.get_webpage_text(link)["content"]
            ids = [link]
            docs = [result_text]
            metas = [
                {"source": link}
            ]
            collection.add(ids=ids, documents=docs, metadatas=metas)

    def save_full_article_to_db(self,link,article_text):
        """"
        Saves the article text to the database
        """
        articles_db=os.getenv("ARTICLES_DB")
        client = chromadb.PersistentClient(path=self.db_path)
        embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=os.getenv("MODEL_NAME")
        )
        collection = client.get_or_create_collection(
            name=articles_db,
            embedding_function=embedder,
            metadata={"hnsw:space": "cosine"}
        )

        ids=[link]

        docs=[article_text]
        metas=[
            {"source": "rss", "link": link}
        ]
        collection.add(ids=ids, documents=docs, metadatas=metas)


    def index_rss_items(self,feeds):
        """
        saves the relevant data from the rss feed
        """
        client = chromadb.PersistentClient(path=self.db_path)
        embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=os.getenv("MODEL_NAME")
        )
        collection = client.get_or_create_collection(
            name=self.db_name,
            embedding_function=embedder
        )
        for feed in feeds:
            self.__index_rss_item(feed, collection)

    def __index_rss_item(self, feed,vector_collection):
        """"
        saves the relevant data from the rss feed
        """
        try:
            text = f"{feed['title']}\n\n{feed['summary']}"
            metadata = {
                "link": feed["link"]
            }

            vector_collection.add(
                ids=[feed["link"]],
                documents=[text],
                metadatas=[metadata]
            )
        except Exception as e:
            print(e)

    def QueryDb(self, query):
        """"
        querries the db for the most relevant rss feed
        """
        client = chromadb.PersistentClient(path=self.db_path)
        embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=os.getenv("MODEL_NAME")
        )
        collection = client.get_collection(
            name=self.db_name,
            embedding_function=embedder
        )

        results = collection.query(
            query_texts=[query],
            n_results=5,
        )

        most_likely_links = [
            {"id": doc, "distance": dist}
            for doc, dist in zip(
                results["ids"][0],
                results["distances"][0]
            )
            if dist < 0.5
        ]

        if len(most_likely_links)==0:
            return {"result":False}
        return {"result":True, "most_likely_links":most_likely_links}

