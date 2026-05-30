from langchain_community.llms import Ollama

llm = Ollama(
    model="llama3",
    temperature=0
)