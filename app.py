import streamlit as st

from agent import run_agent
from tools import load_system_state
from monitor import check_infrastructure


st.set_page_config(
    page_title="NovaTech AI",
    page_icon="🤖",
    layout="centered"
)


st.title("🤖 NovaTech AI Operations Agent")

st.caption(
    "Agentic AI practice project — "
    "NovaTech infrastructure monitoring"
)

st.divider()


# -------------------------------------------------
# INFRASTRUCTURE DASHBOARD
# -------------------------------------------------

st.subheader("🖥️ Infrastructure Status")

system_state = load_system_state()

for system_name, details in system_state.items():

    status = details["status"]
    response_time = details["response_time_ms"]

    if status.lower() == "healthy":
        icon = "🟢"
    else:
        icon = "🔴"

    st.write(
        f"{icon} **{system_name.upper()}** — "
        f"{status.upper()} — "
        f"{response_time} ms"
    )


st.divider()


# -------------------------------------------------
# INCIDENT MONITOR
# -------------------------------------------------

st.subheader("🚨 Incident Monitor")

incidents = check_infrastructure()

if not incidents:

    st.success(
        "No active incidents. "
        "All systems are operating normally."
    )

else:

    st.error(
        f"{len(incidents)} active incident(s) detected."
    )

    for incident in incidents:

        st.warning(
            f"""
**System:** {incident['system'].upper()}

**Status:** {incident['status'].upper()}

**Response Time:** {incident['response_time_ms']} ms
"""
        )


st.divider()


# -------------------------------------------------
# AI AGENT CHAT
# -------------------------------------------------

st.subheader("💬 Talk to NovaTech Agent")


if "messages" not in st.session_state:

    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


user_input = st.chat_input(
    "Ask NovaTech Agent..."
)


if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):

        st.markdown(user_input)


    with st.chat_message("assistant"):

        with st.spinner(
            "Agent is investigating..."
        ):

            try:

                answer = run_agent(user_input)

            except Exception as error:

                answer = (
                    f"Agent error: {error}"
                )

        st.markdown(answer)


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
