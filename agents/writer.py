from utils.llm import llm


def writer_agent(state):

    query = state["query"]

    research = "\n".join(
        state["search_results"]
    )

    critique = state["critique"]

    prompt = f"""
    Write a detailed research report.

    Original Query:
    {query}

    Research Findings:
    {research}

    Critic Feedback:
    {critique}

    Improve the report using the critique.

    Structure:
    - Introduction
    - Key Findings
    - Challenges
    - Future Directions
    - Conclusion
    """

    response = llm.invoke(prompt)

    return {
        "final_report": response.content
    }