from utils.search import search_web


def researcher_agent(state):

    subquestions = state["subquestions"]

    all_results = []

    for question in subquestions:

        results = search_web(question)

        combined = "\n".join(results)

        all_results.append(
            f"""
Research Question:
{question}

Findings:
{combined}
"""
        )

    return {
        "search_results": all_results
    }