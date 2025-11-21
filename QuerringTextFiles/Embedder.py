from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
import  os

class Embedder:
    def __init__(self):
        load_dotenv()
        self.Ollama_Url = os.getenv("ollama_url")
        self.embedding_model = os.getenv("embedding_model")

    # creates Faiss vector object
    def get_embeddings(self,texts:list[str])->FAISS:
        embeddings = OllamaEmbeddings(
            model=self.embedding_model,
            base_url=self.Ollama_Url
        )
        return FAISS.from_texts(texts, embeddings)
