from utils.llm import llm


def critic_agent(state):

    report = state["search_results"]

    combined = "\n\n".join(report)

    prompt = f"""
You are a strict research critic.

Review the following research findings.

Identify:
- missing areas
- weak arguments
- lack of technical depth
- missing examples
- poor structure

Give concise feedback in bullet points.

Research:
{combined}
"""

    response = llm.invoke(prompt)

    return {
        "critique": response.content
    }