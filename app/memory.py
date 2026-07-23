import os
from mem0 import Memory

def get_memory_client():
    config = {
        "llm": {
            "provider": "gemini",
            "config": {
                "model": "gemini-3.1-flash-lite",
                "api_key": os.getenv("GOOGLE_API_KEY"),
                "temperature": 0.2,
                "max_tokens": 2000,
            }
        },
        "embedder": {
            "provider": "gemini",
            "config": {
                "model": "models/gemini-embedding-001",
                "api_key": os.getenv("GOOGLE_API_KEY"),
            }
        },
      "vector_store": {
            "provider": "qdrant",
            "config": {
                "host": os.getenv("QDRANT_HOST", "qdrant"),
                "port": int(os.getenv("QDRANT_PORT", 6333)),
                "embedding_model_dims": 768,
            }
        },
    }
    return Memory.from_config(config)