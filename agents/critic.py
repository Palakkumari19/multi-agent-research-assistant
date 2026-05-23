from utils.llm import llm


def critic_agent(state):

    research = "\n".join(
        state["search_results"]
    )

    prompt = f"""
    Review this research.

    Identify:
    - missing information
    - weak points
    - factual concerns
    - completeness score out of 10

    Research:
    {research}
    """

    response = llm.invoke(prompt)

    return {
        "critique": response.content
    }