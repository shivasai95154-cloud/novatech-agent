import os

from langchain_groq import ChatGroq


def get_groq_api_key():
    # First try a normal environment variable.
    api_key = os.getenv("GROQ_API_KEY")

    if api_key:
        return api_key

    # If running on Streamlit Cloud, try Streamlit Secrets.
    try:
        import streamlit as st

        if "GROQ_API_KEY" in st.secrets:
            return st.secrets["GROQ_API_KEY"]

    except Exception:
        pass

    return None


def create_llm():
    api_key = get_groq_api_key()

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. "
            "Add it to your environment or Streamlit Secrets."
        )

    return ChatGroq(
        api_key=api_key,
        model="openai/gpt-oss-20b",
        temperature=0
    )


def main():
    print("Starting NovaTech Agent...")

    llm = create_llm()

    response = llm.invoke(
        "You are NovaTech's IT Operations AI. "
        "Reply with exactly: NovaTech Agent is online."
    )

    print(response.content)


if __name__ == "__main__":
    main()
