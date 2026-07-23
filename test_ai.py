from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Unlock the Secret Vault
load_dotenv()

# 2. Connect to the Gemini brain (Free Tier)
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash")
# 3. Send a messagec
print("Thinking...")
response = llm.invoke("Say 'Hello World, my AI brain is online!'")

# 4. Print the answer
print(response.content)