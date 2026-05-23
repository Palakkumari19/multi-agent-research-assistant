from utils.llm import llm


def planner_agent(state):

    query = state["query"]

    prompt = f"""
You are an expert research planning agent.

Break the research request into 3-5 focused research questions.

RULES:
- Keep questions specific
- Avoid vague wording
- Cover technical, practical, and future aspects
- Output ONLY bullet points

Research Request:
{query}
"""

    response = llm.invoke(prompt)

    lines = response.content.split("\n")

    questions = []

    for line in lines:

        cleaned = (
            line.replace("-", "")
            .replace("*", "")
            .strip()
        )

        if cleaned:

            questions.append(cleaned)

    state["subquestions"] = questions

    return state