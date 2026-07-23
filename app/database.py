import os
from langchain_neo4j import Neo4jGraph


def get_knowledge_graph():
    """
    Initializes a Neo4j connection that can use APOC procedures when enabled.
    """
    return Neo4jGraph(
        url=os.getenv("NEO4J_URI", "bolt://neo4j:7687"),
        username=os.getenv("NEO4J_USER", "neo4j"),
        password=os.getenv("NEO4J_PASSWORD", "password123"),
    )