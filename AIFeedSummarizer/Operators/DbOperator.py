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
            model_name="all-MiniLM-L6-v2"
        )