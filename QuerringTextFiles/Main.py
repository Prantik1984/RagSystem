from TextOperator import TextOperator # Custom class to load & clean documents
from Embedder import Embedder # Custom embedding generator using Ollama/FAISS
import os
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama # LLM interface via Ollama
from langchain_core.output_parsers import StrOutputParser

# -----------------------------------------------------------
# Entry point of the script. Handles:
# 1. Displaying list of documents located in /data folder
# 2. Allowing user to select a document
# 3. Processing & embedding the selected document
# 4. Accepting user query and fetching relevant context via retriever
# 5. Passing context + query to LLM and printing response
# -----------------------------------------------------------
def main():
    current_dir = Path(__file__).parent
    data_folder = current_dir / "data"
    docs=get_docs_list(data_folder)

    print("Available Documents:")

    for index, filename in docs.items():
        print(f"{index}. {filename}")

    print("Enter number like 1/2/3 to select document to query")

    while True:
        try:
          user_choice = int(input("Enter File Number:"))
          if user_choice in docs:
            break
        except ValueError:
            print("Invalid Input")

    text_operator = TextOperator(os.path.join(data_folder, docs[user_choice]))
    texts=text_operator.load_document()

    embedder=Embedder()
    vector=embedder.get_embeddings(texts)
    retriever=vector.as_retriever(search_kwargs={"k": 2})

    query=input("Ask any question about concerning the text in the selected document:")
    docs=retriever.invoke(query)

    prompt = ChatPromptTemplate.from_template(
        "Please use the following docs:\n{docs}\n\n"
        "to answer the question:\n{query}"
    )

    llm = ChatOllama(model="llama3.2:latest")
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"docs": docs, "query": query})
    print(f"Answer::: \n \n{response}")

def get_docs_list(folder_path:str) -> list:
    return {
        i: file.name
        for i, file in enumerate(Path(folder_path).iterdir(), start=1)
        if file.is_file()}


if __name__ == "__main__":
    main()