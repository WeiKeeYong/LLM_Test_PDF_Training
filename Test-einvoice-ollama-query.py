import argparse
import re
import datetime
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from get_embedding_function import get_embedding_function


CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
If User ask in Bahasa Melayu i will answer using Bahasa Melayu, If User ask in English  i will answer using English, If User ask in Chinese  i will answer using Chinese, 

---

Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def query_rag(query_text: str, db):
    results = db.similarity_search_with_score(query_text, k=20)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text, dt_now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    #model = Ollama(base_url='http://127.0.0.1:11434', model="mistral")
    model = Ollama(base_url='http://34.132.82.86:11434',model="llama3") #wizardlm2,llama3,llama3:text,phi3
    response_text = model.invoke(prompt)
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    #formatted_response = f"Response: {response_text}\nSources: {sources}"
    formatted_response = f"Response: \n{response_text}"
    return formatted_response


# Initialize embedding function and Chroma database
embedding_function = get_embedding_function()
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

while True:
    query_text = input("\nEnter your query (type 'exit' to quit): ").strip()

    if query_text.lower() == 'exit':
        print("Exiting...")
        break

    response = query_rag(query_text, db)
    #print(response)
    print("\n------Response from AI Agent-- this is a test, NOT REAL-----\n\n" + response + "\n\n--------------End of AI Agent Response--------------")


'''
import argparse
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama

from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)


def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)

    model = Ollama(base_url='http://127.0.0.1:11434', model="mistral")
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text


if __name__ == "__main__":
    main()

'''