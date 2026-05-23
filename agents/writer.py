from utils.llm import llm


def writer_agent(state):

    query = state["query"]

    findings = "\n\n".join(
        state["search_results"]
    )[:3000]

    critique = state["critique"]

    prompt = f"""
You are an expert research report writer.

Write a WELL-FORMATTED research report.

IMPORTANT RULES:
- Use proper markdown headings
- Use short paragraphs
- Use bullet points where useful
- NO markdown symbols like **
- NO code blocks
- Make it clean and readable
- Include examples
- Keep formatting professional

Research Topic:
{query}

Research Findings:
{findings}

Critic Feedback:
{critique}

Generate a polished final report.
"""

    response = llm.invoke(prompt)

    return {
        "final_report": response.content
    }