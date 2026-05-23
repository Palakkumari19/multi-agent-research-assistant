from utils.llm import llm


def planner_agent(state):

    query = state["query"]

    prompt = f"""
You are a research planning expert.

Break the following research query into
3-5 focused research subquestions.

Research Query:
{query}

Return ONLY bullet points.
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