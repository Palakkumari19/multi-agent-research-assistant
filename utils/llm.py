
from langchain_groq import ChatGroq

from utils.config import get_secret

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=get_secret(
        "GROQ_API_KEY"
    )
)