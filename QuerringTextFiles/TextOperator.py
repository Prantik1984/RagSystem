from langchain_community.document_loaders import TextLoader as LangLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import  os
import re
from dotenv import load_dotenv

class TextOperator:
    def __init__(self,filepath:str):
        load_dotenv()
        self.querriablefile = filepath

# loads the text from document
# cleans it
# returns the text
    def load_document(self)->list[str]:
        documents = LangLoader(self.querriablefile).load()
        chunk_size = int(os.getenv("CHUNK_SIZE"))
        chunk_overlap = int(os.getenv("chunk_overlap"))
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        texts = text_splitter.split_documents(documents)
        texts = [self.clean_text(text.page_content) for text in texts]
        return texts

# returns a lowercased, space-normalized string containing only alphabetic characters.
    def clean_text(self, txt):
        txt = re.sub(r"[^a-zA-Z\s]", "", txt)
        txt = re.sub(r"\s+", " ", txt).strip()
        txt = txt.lower()
        return txt
