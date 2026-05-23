from utils.search import search_web
from utils.llm import llm


def researcher_agent(state):

    subquestions = state["subquestions"]

    findings = []

    for question in subquestions:

        web_results = search_web(question)

        summarized_results = []

        for result in web_results:

            summary_prompt = f"""
Summarize this research result clearly.

Keep it concise and readable.

Content:
{result}
"""

            summary = llm.invoke(
                summary_prompt
            ).content

            summarized_results.append(summary)

        findings.append(
            f"""
### Research Question
{question}

### Findings
{" ".join(summarized_results)}
"""
        )

    state["search_results"] = findings

    return state