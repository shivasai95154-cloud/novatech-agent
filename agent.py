import os

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from tools import check_system_health


def get_groq_api_key():
    api_key = os.getenv("GROQ_API_KEY")

    if api_key:
        return api_key

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


TOOLS = [check_system_health]

TOOL_MAP = {
    "check_system_health": check_system_health
}


def run_agent(user_message: str):
    llm = create_llm()

    # Give our tool definitions to the model.
    llm_with_tools = llm.bind_tools(TOOLS)

    messages = [
        SystemMessage(
            content=(
                "You are NovaTech's autonomous IT Operations Agent. "
                "You have tools for inspecting company infrastructure. "
                "When a user asks about the health, status, availability, "
                "or performance of a NovaTech system, use the appropriate "
                "tool instead of guessing. "
                "After receiving the tool result, explain the result clearly."
            )
        ),
        HumanMessage(content=user_message)
    ]

    # STEP 1:
    # Let the LLM decide whether it needs a tool.
    response = llm_with_tools.invoke(messages)

    messages.append(response)

    # STEP 2:
    # Execute tools requested by the LLM.
    if response.tool_calls:

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            if tool_name not in TOOL_MAP:
                continue

            selected_tool = TOOL_MAP[tool_name]

            tool_result = selected_tool.invoke(tool_args)

            messages.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call["id"]
                )
            )

        # STEP 3:
        # Give observations back to the LLM.
        final_response = llm_with_tools.invoke(messages)

        return final_response.content

    # No tool was necessary.
    return response.content


def main():
    result = run_agent(
        "What is the current status of the NovaTech VPN?"
    )

    print(result)


if __name__ == "__main__":
    main()
