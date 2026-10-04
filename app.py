import streamlit as st

from agent import run_agent


st.set_page_config(
    page_title="NovaTech AI",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 NovaTech AI Operations Agent")

st.caption(
    "Agentic AI practice project — NovaTech infrastructure monitoring"
)

st.divider()


if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages.
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input.
user_input = st.chat_input(
    "Ask about NovaTech infrastructure..."
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

        with st.spinner("Agent is investigating..."):

            try:
                answer = run_agent(user_input)

            except Exception as error:
                answer = f"Agent error: {error}"

        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
