from utils.llm import llm


def critic_agent(state):

    findings = state["search_results"]

    previous_report = state.get(
        "final_report",
        ""
    )

    prompt = f"""
You are a strict research critic.

Analyze the research quality.

Identify:
- Missing information
- Weak explanations
- Missing technical depth
- Missing examples
- Missing future directions

Also suggest EXACT improvements.

Previous Report:
{previous_report}

Research Findings:
{findings}
"""

    response = llm.invoke(prompt)

    state["critique"] = response.content

    return state