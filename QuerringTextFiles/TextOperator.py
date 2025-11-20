from langchain_community.document_loaders import TextLoader as LangLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import  os
from dotenv import load_dotenv
class TextOperator:
    def __init__(self,filepath:str):
        load_dotenv()
        self.querriablefile = filepath


    def load_document(self):
        documents = LangLoader(self.querriablefile).load()
        chunk_size = int(os.getenv("CHUNK_SIZE"))
        chunk_overlap = int(os.getenv("chunk_overlap"))
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        texts = text_splitter.split_documents(documents)

        print(texts)
