from newspaper import Article
from langchain_text_splitters import RecursiveCharacterTextSplitter
class Chunker:
    def chunk_text(self,article:Article):
      """"
      creates chunks of text from article
      """
      article_text=article.text

      text_splitter = RecursiveCharacterTextSplitter(
          chunk_size=500,
          chunk_overlap=100
      )

      texts = text_splitter.split_text(article_text)
      return texts

