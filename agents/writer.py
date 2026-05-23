from utils.llm import llm

def writer_agent(state):

    query = state["query"]

    search_results = state["search_results"]

    critique = state["critique"]

    prompt = f"""
You are a professional AI research report writer.

Write a WELL-FORMATTED markdown research report.

IMPORTANT FORMATTING RULES:

- Use proper markdown headings:
# Title
## Introduction
## Key Findings
## Challenges
## Future Directions
## Conclusion
## Recommendations

- Use bullet points where needed.
- Use short readable paragraphs.
- Add spacing between sections.
- Do NOT write everything in one paragraph.
- Make the report visually clean and professional.

Research Query:
{query}

Research Findings:
{search_results}

Critique:
{critique}

Generate the final report now.
"""

    response = llm.invoke(prompt)

    state["final_report"] = response.content

    return state