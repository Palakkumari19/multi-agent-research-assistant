from utils.llm import llm


def writer_agent(state):

    query = state["query"]

    findings = state["search_results"]

    critique = state["critique"]

    previous_report = state.get(
        "final_report",
        ""
    )

    prompt = f"""
You are an expert research writer.

Your task:
1. Improve the research using critic feedback
2. Generate a polished markdown report
3. Clearly summarize what improvements were added

IMPORTANT:
- Use proper markdown
- Use headings
- Use bullet points
- Keep spacing clean
- NO raw markdown symbols like **

FIRST generate:
# Improvements Added

THEN generate:
# Final Research Report

Research Query:
{query}

Previous Report:
{previous_report}

Research Findings:
{findings}

Critic Feedback:
{critique}
"""

    response = llm.invoke(prompt)

    content = response.content

    if "# Final Research Report" in content:

        parts = content.split(
            "# Final Research Report"
        )

        improvement_summary = parts[0]

        final_report = (
            "# Final Research Report\n"
            + parts[1]
        )

    else:

        improvement_summary = ""

        final_report = content

    state["improvement_summary"] = (
        improvement_summary
    )

    state["final_report"] = final_report

    return state