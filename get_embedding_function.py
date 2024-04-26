from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings

#this to use for generating embedding aka vector use it for embedding document into Vector. 

def get_embedding_function():
    '''
    embeddings = BedrockEmbeddings(
        credentials_profile_name="default", region_name="us-east-1"
    )'''
    #embeddings = OllamaEmbeddings(model="nomic-embed-text")
    embeddings = OllamaEmbeddings(base_url='http://34.132.82.86:11434',model="nomic-embed-text")
    #embeddings = OllamaEmbeddings(base_url='http://35.224.59.94:11434',model="llama3")
    return embeddings