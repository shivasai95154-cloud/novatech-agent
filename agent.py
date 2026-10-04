import os

from langchain_groq import ChatGroq


def create_llm():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Add it as an environment variable."
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
