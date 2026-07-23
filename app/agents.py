import os
from langchain_google_genai import ChatGoogleGenerativeAI

from app.memory import get_memory_client
from app.message_utils import extract_text_content

memory_client = get_memory_client()


def call_model(state: dict):
    llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")
    messages = state.get("messages", [])

    last = messages[-1] if messages else ""
    raw_content = last.content if hasattr(last, "content") else last
    user_input = extract_text_content(raw_content)

    user_id = "ashish_user"
    relevant_memories = memory_client.search(query=user_input, filters={"user_id": user_id})
    memories_list = relevant_memories.get("results", []) if isinstance(relevant_memories, dict) else relevant_memories

    context_str = "\n".join([m["memory"] for m in memories_list]) if memories_list else "No prior memory."
    enhanced_prompt = f"User Profile / Past Memories:\n{context_str}\n\nCurrent User Message: {user_input}"

    response = llm.invoke(enhanced_prompt)
    memory_client.add(user_input, user_id=user_id)
    return {"messages": [response]}
