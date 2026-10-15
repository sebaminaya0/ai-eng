"""Streamlit chat UI for the 13.03 API. Built in 13.04.

    uv run uvicorn app:app --port 8765 &      # the API
    uv run streamlit run ui_streamlit.py      # UI on http://localhost:8501
"""
import streamlit as st

from ui_gradio import stream_answer  # same SSE client, different UI

st.title("mini-wiki RAG")
st.caption("Answers from 3.2k Wikipedia passages, with citations.")

if "messages" not in st.session_state:
    st.session_state.messages = []  # Streamlit reruns the whole script on every interaction: state lives here

for m in st.session_state.messages:
    st.chat_message(m["role"]).markdown(m["content"])

if question := st.chat_input("Ask about the corpus"):
    st.chat_message("user").markdown(question)
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("assistant"):
        box, text, sources = st.empty(), "", []
        for text, sources in stream_answer(question):
            box.markdown(text + "▌")
        box.markdown(text)
        if sources:
            st.caption(f"sources: {', '.join(map(str, sources))}")
    st.session_state.messages.append({"role": "assistant", "content": text})
