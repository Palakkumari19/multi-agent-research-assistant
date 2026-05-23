from utils.search import search_web
from utils.llm import llm


def researcher_agent(state):

    subquestions = state["subquestions"]

    findings = []

    for question in subquestions:

        web_results = search_web(question)

        combined = "\n".join(web_results[:2])

        summary_prompt = f"""
You are a research summarization agent.

Summarize the findings clearly.

FORMAT:
- Key Insights
- Important Technologies
- Applications
- Challenges

Keep response readable and concise.

Research Question:
{question}

Search Results:
{combined}
"""

        summary = llm.invoke(
            summary_prompt
        ).content

        findings.append(
            f"""
## Research Question
{question}

## Findings
{summary}
"""
        )

    state["search_results"] = findings

    return state