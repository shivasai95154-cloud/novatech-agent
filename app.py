import streamlit as st

from agent import run_agent, analyze_incident
from tools import load_system_state
from monitor import process_incidents
from incident_db import get_all_incidents


st.set_page_config(
    page_title="NovaTech AI",
    page_icon="🤖",
    layout="centered"
)


st.title(
    "🤖 NovaTech AI Operations Agent"
)

st.caption(
    "Agentic AI practice project — "
    "NovaTech infrastructure monitoring"
)

st.divider()


# -------------------------------------------------
# PROCESS INFRASTRUCTURE
# -------------------------------------------------

monitor_results = process_incidents()


# -------------------------------------------------
# NEW INCIDENT ANALYSIS
# -------------------------------------------------

for incident in monitor_results["new"]:

    ai_incident = {
        "system": incident["system"],
        "status": incident[
            "detected_status"
        ],
        "response_time_ms": incident[
            "response_time_ms"
        ]
    }


    try:

        analysis = analyze_incident(
            ai_incident
        )

        st.error(
            f"🚨 New incident detected: "
            f"{incident['incident_number']}"
        )

        st.markdown(
            "#### 🤖 AI Incident Analysis"
        )

        st.markdown(
            analysis
        )


    except Exception as error:

        st.error(
            f"AI incident analysis failed: "
            f"{error}"
        )


# -------------------------------------------------
# RECOVERY NOTIFICATION
# -------------------------------------------------

for incident in monitor_results["resolved"]:

    st.success(
        f"✅ {incident['incident_number']} "
        f"has been resolved. "
        f"{incident['system'].upper()} "
        f"is healthy again."
    )


# -------------------------------------------------
# INFRASTRUCTURE DASHBOARD
# -------------------------------------------------

st.subheader(
    "🖥️ Infrastructure Status"
)


system_state = load_system_state()


for system_name, details in system_state.items():

    status = details[
        "status"
    ]

    response_time = details[
        "response_time_ms"
    ]


    if status.lower() == "healthy":

        icon = "🟢"

    else:

        icon = "🔴"


    st.write(
        f"{icon} "
        f"**{system_name.upper()}** — "
        f"{status.upper()} — "
        f"{response_time} ms"
    )


st.divider()


# -------------------------------------------------
# INCIDENT DATABASE
# -------------------------------------------------

st.subheader(
    "🚨 Incident History"
)


incident_history = get_all_incidents()


if not incident_history:

    st.success(
        "No incidents have been recorded."
    )


else:

    for incident in incident_history:

        if (
            incident["incident_status"]
            == "OPEN"
        ):

            icon = "🔴"

        else:

            icon = "✅"


        st.markdown(
            f"""
{icon} **{incident['incident_number']}**

**System:** {incident['system'].upper()}

**Detected Status:** {incident['detected_status'].upper()}

**Incident Status:** {incident['incident_status']}

**Detected:** {incident['detected_at']}

---
"""
        )


st.divider()


# -------------------------------------------------
# AI CHAT
# -------------------------------------------------

st.subheader(
    "💬 Talk to NovaTech Agent"
)


if "messages" not in st.session_state:

    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


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

        st.markdown(
            user_input
        )


    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "Agent is investigating..."
        ):

            try:

                answer = run_agent(
                    user_input
                )

            except Exception as error:

                answer = (
                    f"Agent error: "
                    f"{error}"
                )


        st.markdown(
            answer
        )


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
