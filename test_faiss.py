from memory.faiss_store import (
    store_memory,
    retrieve_similar
)

store_memory(
    "What is RAG?",
    "RAG combines retrieval with generation."
)

store_memory(
    "Explain AI agents",
    "AI agents perform autonomous tasks."
)

results = retrieve_similar(
    "Recent retrieval augmented generation systems"
)

print(results)