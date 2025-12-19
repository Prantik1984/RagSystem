import os
from dotenv import load_dotenv
class LLMSummarizer:
    def __init__(self):
        load_dotenv()
        self.ollama_url=os.getenv("OLLAMA_URL")
        self.prompt=""""
        You are a professional news analyst.
        
        Summarize the following news article into a maximum of 10 concise bullet points.
        
        Guidelines:
        - Each point must capture a key fact, insight, or development.
        - Be factual and neutral; do not add opinions or speculation.
        - Avoid repetition or minor details.
        - Keep each bullet point to one or two short sentences.
        - Focus on: who, what, why it matters, and future implications (if mentioned).
        - Do NOT exceed 10 bullet points.
        
        Article:
        \"\"\"
        {ARTICLE_TEXT}
        \"\"\"
        """

    def summarize_article(self,article_text:str)->str:
        """"
        creates a 10 point summary of the article
        """
        # prompt =self.prompt.format(article=article_text)
        return "Hello"