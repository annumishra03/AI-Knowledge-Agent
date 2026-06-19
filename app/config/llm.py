import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    streaming=True,
    api_key=os.getenv("API_KEY"),
    temperature=0
)