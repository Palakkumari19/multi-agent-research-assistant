from graph.workflow import app

query = """
Summarize recent AI research on RAG systems
"""

result = app.invoke({
    "query": query,
    "subquestions": [],
    "search_results": [],
    "critique": "",
    "final_report": ""
})

print(result["final_report"])