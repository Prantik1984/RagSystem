import os
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions

class DbOperator:
    def __init__(self):
        load_dotenv()
        self.db_name = os.getenv("DB_NAME")
        self.db_path = os.getenv("DB_PATH")

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
            n_results=1,
        )

        print(results)

