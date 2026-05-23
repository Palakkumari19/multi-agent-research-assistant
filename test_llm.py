from utils.llm import llm

response = llm.invoke("Explain RAG in one paragraph")

print(response.content)