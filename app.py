import streamlit as st
from core.job_orchestrator import JobOrchestrator

st.set_page_config(page_title="JobGPT - Find Jobs", page_icon="🧑‍💻", layout="centered")

st.title("JobGPT 🧑‍💻")
st.write("Hi! Ask me about jobs you are looking for.")

if "orch" not in st.session_state:
    st.session_state.orch = JobOrchestrator()

user_input = st.text_input("Your request:", key="input")
if st.button("Find Jobs"):
    if user_input.strip():
        response = st.session_state.orch.handle(user_input)
        st.markdown(response)
    else:
        st.warning("Please enter something!")
