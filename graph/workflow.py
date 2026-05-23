from langgraph.graph import StateGraph, END

from graph.state import ResearchState

from agents.planner import planner_agent
from agents.researcher import researcher_agent
from agents.critic import critic_agent
from agents.writer import writer_agent


graph = StateGraph(ResearchState)

graph.add_node("planner", planner_agent)

graph.add_node(
    "researcher",
    researcher_agent
)

graph.add_node(
    "critic",
    critic_agent
)

graph.add_node(
    "writer",
    writer_agent
)

graph.set_entry_point("planner")

graph.add_edge(
    "planner",
    "researcher"
)

graph.add_edge(
    "researcher",
    "critic"
)

graph.add_edge(
    "critic",
    "writer"
)

graph.add_edge(
    "writer",
    END
)

app = graph.compile()