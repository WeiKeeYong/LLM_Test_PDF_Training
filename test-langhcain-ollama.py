from langchain_community.llms import Ollama

llm = Ollama(base_url='http://127.0.0.1:11434', model='llama2')  # can remover base_url if run local, if hosted ollama on another ip, replace with the correct ip e.g. http://172.19.1.122:14434

joke = llm.invoke('Tell me two jokes Chinese')
print(joke)
