import os

from langchain_groq import ChatGroq
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    ToolMessage
)

from tools import check_system_health


# -------------------------------------------------
# API KEY
# -------------------------------------------------

def get_groq_api_key():

    # Try normal environment variable first
    api_key = os.getenv("GROQ_API_KEY")

    if api_key:
        return api_key

    # Try Streamlit Secrets
    try:
        import streamlit as st

        if "GROQ_API_KEY" in st.secrets:
            return st.secrets["GROQ_API_KEY"]

    except Exception:
        pass

    return None


# -------------------------------------------------
# CREATE LLM
# -------------------------------------------------

def create_llm():

    api_key = get_groq_api_key()

    if not api_key:

        raise ValueError(
            "GROQ_API_KEY is missing. "
            "Add it to Streamlit Secrets."
        )

    return ChatGroq(
        api_key=api_key,
        model="openai/gpt-oss-20b",
        temperature=0
    )


# -------------------------------------------------
# AGENT TOOLS
# -------------------------------------------------

TOOLS = [
    check_system_health
]


TOOL_MAP = {
    "check_system_health": check_system_health
}


# -------------------------------------------------
# INTERACTIVE AGENT
# -------------------------------------------------

def run_agent(user_message: str):
    """
    Interactive NovaTech agent.

    The LLM decides whether it needs to call
    infrastructure tools before answering.
    """

    llm = create_llm()

    llm_with_tools = llm.bind_tools(
        TOOLS
    )

    messages = [

        SystemMessage(
            content=(
                "You are NovaTech's autonomous "
                "IT Operations Agent. "

                "You have tools for inspecting "
                "NovaTech infrastructure. "

                "When a user asks about the health, "
                "status, availability, or performance "
                "of a NovaTech system, use the "
                "appropriate tool instead of guessing. "

                "After receiving the tool result, "
                "explain the result clearly."
            )
        ),

        HumanMessage(
            content=user_message
        )

    ]

    # ---------------------------------------------
    # LET LLM DECIDE WHETHER TO USE A TOOL
    # ---------------------------------------------

    response = llm_with_tools.invoke(
        messages
    )

    messages.append(response)


    # ---------------------------------------------
    # EXECUTE REQUESTED TOOLS
    # ---------------------------------------------

    if response.tool_calls:

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]

            tool_args = tool_call["args"]


            if tool_name not in TOOL_MAP:

                continue


            selected_tool = TOOL_MAP[
                tool_name
            ]


            tool_result = selected_tool.invoke(
                tool_args
            )


            messages.append(

                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call["id"]
                )

            )


        # -----------------------------------------
        # RETURN TOOL RESULTS TO LLM
        # -----------------------------------------

        final_response = (
            llm_with_tools.invoke(
                messages
            )
        )

        return final_response.content


    # No tool was required
    return response.content


# -------------------------------------------------
# AUTOMATIC INCIDENT ANALYSIS
# -------------------------------------------------

def analyze_incident(
    incident: dict
) -> str:

    """
    Analyze an infrastructure incident that was
    automatically detected by the monitoring system.

    This does NOT require the user to ask a question.
    """

    llm = create_llm()


    system_name = incident[
        "system"
    ]

    status = incident[
        "status"
    ]

    response_time = incident[
        "response_time_ms"
    ]


    prompt = f"""
You are NovaTech's autonomous IT Operations Incident Analyst.

The NovaTech monitoring system has automatically
detected an infrastructure incident.

INCIDENT DATA

System: {system_name}
Status: {status}
Response Time: {response_time} ms


Analyze the incident.

Return a concise incident report containing
exactly these sections:

Severity:
Business Impact:
Likely Cause:
Recommended Action:


Severity must be exactly one of:

LOW
MEDIUM
HIGH
CRITICAL


IMPORTANT:

Do not claim that you restarted services,
fixed systems, contacted employees,
created tickets, or performed other actions
unless those actions were actually performed.

Your job at this stage is only to analyze
the detected incident.
"""


    response = llm.invoke(
        prompt
    )


    return response.content


# -------------------------------------------------
# MONITOR CONNECTION
# -------------------------------------------------

def analyze_detected_incident(
    incident: dict
) -> str:

    return analyze_incident(
        incident
    )


# -------------------------------------------------
# LOCAL TEST
# -------------------------------------------------

def main():

    print(
        "Starting NovaTech Agent..."
    )


    result = run_agent(
        "What is the current status "
        "of the NovaTech VPN?"
    )


    print(result)


if __name__ == "__main__":

    main()
