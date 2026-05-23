from langgraph.graph import (
    StateGraph,
    END
)

from graph.state import ResearchState

from agents.planner import planner_agent
from agents.researcher import researcher_agent
from agents.critic import critic_agent
from agents.writer import writer_agent

workflow = StateGraph(
    ResearchState
)

workflow.add_node(
    "planner",
    planner_agent
)

workflow.add_node(
    "researcher",
    researcher_agent
)

workflow.add_node(
    "critic",
    critic_agent
)

workflow.add_node(
    "writer",
    writer_agent
)

workflow.set_entry_point(
    "planner"
)

workflow.add_edge(
    "planner",
    "researcher"
)

workflow.add_edge(
    "researcher",
    "critic"
)

workflow.add_edge(
    "critic",
    "writer"
)

workflow.add_edge(
    "writer",
    END
)

app = workflow.compile()