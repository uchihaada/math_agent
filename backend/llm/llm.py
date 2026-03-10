import os

from dotenv import load_dotenv

load_dotenv()


def get_llm():
    from langchain_groq import ChatGroq

    groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not found in environment")

    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model="llama-3.1-8b-instant",
        temperature=0,
    )

    return llm
