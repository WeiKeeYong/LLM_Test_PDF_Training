from langchain_community.llms import Ollama

llm = Ollama(base_url='http://127.0.0.1:11434', model='llama2')

joke = llm.invoke('Tell me two jokes Chinese')
print(joke)