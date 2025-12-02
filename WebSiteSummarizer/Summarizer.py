import requests
import json
class Summarizer:
    OLLAMA_URL = "http://localhost:11434/api/generate"
    MODEL_NAME = "llama3.2:latest"

    def summrizeArticle(self,article_text:str):
        """
        summarizes an article text
        """

        prompt = f"""
        You are an assistant that summarizes news articles.

        Summarize the following article in 5–7 concise bullet points.
        Focus on key facts, numbers, and outcomes. Avoid fluff.

        ARTICLE:
        {article_text}
        """

        payload = {
            "model":self.MODEL_NAME,
            "prompt": prompt,
            "stream": True
        }

        response = requests.post(self.OLLAMA_URL, json=payload, stream=True)
        response.raise_for_status()

        summary_chunks = []

        for line in response.iter_lines():
            if not line:
                continue
            data = line.decode("utf-8")

            try:
                obj = json.loads(data)
                chunk = obj.get("response", "")
                summary_chunks.append(chunk)

            except Exception as e:
                print(e)

        return "".join(summary_chunks).strip()


