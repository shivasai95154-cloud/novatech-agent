import streamlit as st

from agent import create_llm


st.set_page_config(
    page_title="NovaTech AI",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 NovaTech AI Operations Agent")

st.write(
    "Practice project for building a 24/7 Agentic AI "
    "IT Operations and Incident Response System."
)

st.divider()

if st.button("Test AI Agent"):
    try:
        with st.spinner("Contacting NovaTech Agent..."):
            llm = create_llm()

            response = llm.invoke(
                "You are NovaTech's IT Operations AI. "
                "Reply with exactly: NovaTech Agent is online."
            )

        st.success(response.content)

    except Exception as error:
        st.error(f"Agent error: {error}")
