from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from app.agents import call_model
from app.graph_writer import store_enterprise_knowledge

class State(TypedDict):
    messages: Annotated[list, add_messages]

workflow = StateGraph(state_schema=State)

workflow.add_node("oracle", call_model)
workflow.add_node("neo4j_writer", store_enterprise_knowledge)


workflow.add_edge(START, "oracle")
workflow.add_edge("oracle", "neo4j_writer")
workflow.add_edge("neo4j_writer", END)

app_graph = workflow.compile()