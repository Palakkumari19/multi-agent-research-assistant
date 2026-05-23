from utils.search import search_web


def researcher_agent(state):

    subquestions = state["subquestions"]

    all_results = []

    for question in subquestions:

        results = search_web(question)

        combined = "\n\n".join(results[:1])

        formatted = f"""
### Research Question
{question}

### Findings
{combined}
"""

        all_results.append(formatted)

    return {
        "search_results": all_results
    }