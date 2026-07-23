import os
from langchain_google_genai import ChatGoogleGenerativeAI
from app.database import get_knowledge_graph
from app.message_utils import extract_text_content


def _extract_latest_human_input(messages: list) -> str:
    for message in reversed(messages):
        if getattr(message, "type", None) == "human":
            raw_content = getattr(message, "content", "")
            return extract_text_content(raw_content)

    if messages:
        last = messages[-1]
        raw_content = getattr(last, "content", last)
        return extract_text_content(raw_content)

    return ""


def store_enterprise_knowledge(state: dict):
    messages = state.get("messages", [])
    if not messages:
        return {}

    print(f"--- [DEBUG] Neo4j Writer received state: ---{messages}")
    user_input = _extract_latest_human_input(messages)

    print(f"--- [DEBUG] Neo4j Writer received input: {user_input} ---")

    if len(user_input.strip()) < 10:
        print("--- [DEBUG] Skipped: Message too short (< 10 chars) ---")
        return {}

    try:
        driver = get_knowledge_graph()
        llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0)

        prompt = f"""
        Extract key entities and relationships from this text to be stored in a graph database.
        Text: "{user_input}"
        Return ONLY a valid Cypher query using CREATE. Example:
        CREATE (e1:Entity {{name: 'Badminton'}})-[:PLAYS]->(e2:Entity {{name: 'User'}})
        If no relation can be formed, output: NONE
        """

        raw_response = llm.invoke(prompt)
        result = extract_text_content(raw_response.content).strip()
        print(f"--- [DEBUG] Gemini raw Cypher output: {result} ---")

        if "CREATE" in result:
            cypher_query = result.replace("```cypher", "").replace("```", "").strip()
            print(f"--- [DEBUG] Executing Cypher: {cypher_query} ---")
            driver.query(cypher_query)
            print("Successfully wrote to Neo4j!")
        else:
            print("--- [DEBUG] Skipped: Gemini did not return a valid CREATE query ---")

    except Exception as e:
        print(f"*** Neo4j write error: {e} ***")

    return {}