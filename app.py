import streamlit as st
from ingest import load_sample_tickets
from classify import classify_ticket
from rag import answer_query
from dotenv import load_dotenv
import os
load_dotenv()

st.set_page_config(page_title="Customer Support Copilot", layout="wide")
st.title("Customer Support Copilot — intern prototype")
st.markdown("Bulk classify tickets and try a small assistant view.")

@st.cache_data
def load_tickets():
    return load_sample_tickets()

tickets = load_tickets()

# prepare table
rows = []
for t in tickets:
    text = t.get("body","")
    short = text if len(text) < 100 else text[:97] + "..."
    cl = classify_ticket(text)
    rows.append({
        "id": t.get("id"),
        "subject": t.get("subject"),
        "text": short,
        "topic": cl.get("topic"),
        "sentiment": cl.get("sentiment"),
        "priority": cl.get("priority"),
        "confidence": cl.get("confidence","")
    })

st.subheader("Bulk Ticket View")
st.dataframe(rows)

st.markdown("---")
st.subheader("Interactive Ticket / Question")

col1, col2 = st.columns(2)
with col1:
    user_text = st.text_area("Paste a ticket or question here", height=220)
    if st.button("Analyze & Respond"):
        if not user_text.strip():
            st.warning("Write a ticket first.")
        else:
            analysis = classify_ticket(user_text)
            st.session_state["analysis"] = analysis
            st.session_state["last_text"] = user_text
            st.success("Done")

with col2:
    st.write("Internal Analysis View")
    if st.session_state.get("analysis"):
        st.json(st.session_state["analysis"])
    else:
        st.info("Analyze a ticket to see the JSON classification.")

st.markdown("### Final Response")
if st.session_state.get("analysis"):
    topic = st.session_state["analysis"].get("topic")
    q = st.session_state.get("last_text","")
    if topic in {"How-to", "Product", "Best practices", "API/SDK", "SSO"}:
        st.write("Answering using local KB (RAG). Cited URLs shown below.")
        res = answer_query(q)
        st.markdown("**Answer (aggregated):**")
        st.write(res.get("answer"))
        st.markdown("**Cited sources:**")
        for s in res.get("sources",[]):
            st.write(s)
    else:
        st.info(f"This ticket has been classified as '{topic}' and will be routed to the appropriate team.")

st.caption("Set OPENAI_API_KEY in .env to enable LLM-based classification and embeddings. CHROMA_DB_DIR optional.")
