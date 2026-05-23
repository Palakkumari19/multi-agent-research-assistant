from utils.llm import llm


def writer_agent(state):

    query = state["query"]

    search_results = state["search_results"]

    critique = state["critique"]

    prompt = f"""
You are a professional research report writer.

Create a WELL-FORMATTED markdown research report.

IMPORTANT FORMATTING RULES:
- Use proper markdown headings
- Use bullet points
- Use numbered lists where needed
- Leave proper spacing between sections
- NEVER write everything in one paragraph
- NEVER include raw markdown symbols like **
- Keep paragraphs short and readable

FORMAT:

# Final Research Report

## Introduction

## Key Findings

## Critical Analysis

## Challenges

## Future Directions

## Conclusion

Research Query:
{query}

Research Findings:
{search_results}

Critic Feedback:
{critique}
"""

    response = llm.invoke(prompt)

    state["final_report"] = response.content

    return state