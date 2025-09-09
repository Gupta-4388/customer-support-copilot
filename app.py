# app.py
"""
Streamlit app
- dashboard with tickets
- interactive input: shows internal analysis and final response view
- on start, loads sample tickets
"""

import streamlit as st
from pathlib import Path
import json
from ingest import load_sample_tickets
from rag import answer_query

st.set_page_config(page_title="Customer Support Copilot")

st.title("Customer Support Copilot — intern prototype")
st.write("Bulk classify tickets and try a small assistant view.")

# Load sample tickets
tickets = load_sample_tickets()
ticket_dict = {t["id"]: t["subject"] for t in tickets}

ticket_selection = st.selectbox("Select a ticket:", list(ticket_dict.keys()), format_func=lambda x: f"{x}: {ticket_dict[x]}")

st.subheader("Interactive Ticket / Question")
user_input = st.text_area("Paste a ticket or question here", tickets[0]["body"])

if st.button("Done"):
    st.subheader("Internal Analysis View")
    result = answer_query(user_input)
    
    st.json({
        "Answer": result["answer"],
        "Cited source": result["source"]
    })
    
    st.subheader("Final Response")
    st.markdown(f"**Answer (aggregated):** {result['answer']}")
    if result["source"]:
        st.markdown(f"**Cited source:** [Click here]({result['source']})")
