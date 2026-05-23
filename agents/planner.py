from utils.llm import llm


def planner_agent(state):

    query = state["query"]

    prompt = f"""
    Break this research query into 3 focused subquestions.

    Query:
    {query}

    Return only bullet points.
    """

    response = llm.invoke(prompt)

    subquestions = [
        line.replace("-", "").strip()
        for line in response.content.split("\n")
        if line.strip()
    ]

    return {
        "subquestions": subquestions
    }