import faiss
import numpy as np

from utils.embeddings import get_embedding


dimension = 384

index = faiss.IndexFlatL2(dimension)

stored_queries = []
stored_reports = []


def store_memory(query, report):

    embedding = get_embedding(query)

    vector = np.array([embedding]).astype("float32")

    index.add(vector)

    stored_queries.append(query)

    stored_reports.append(report)


def retrieve_similar(query, top_k=2):

    if len(stored_queries) == 0:
        return []

    embedding = get_embedding(query)

    vector = np.array([embedding]).astype("float32")

    distances, indices = index.search(vector, top_k)

    results = []

    for idx in indices[0]:

        if idx < len(stored_reports):

            results.append({
                "query": stored_queries[idx],
                "report": stored_reports[idx]
            })

    return results