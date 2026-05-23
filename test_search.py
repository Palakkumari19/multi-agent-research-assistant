from utils.search import search_web

results = search_web("Latest research on RAG systems")

for r in results:
    print(r)
    print("=" * 50)