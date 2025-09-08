# Customer Support Copilot (Atlan AI Engineer Internship Task)

## 📌 Overview
This repository contains my submission for the **Atlan AI Engineering Internship Challenge**.  
The goal of this task was to build a **Customer Support Copilot** system that can handle ticket classification, knowledge retrieval, and provide a small assistant view for resolving queries.

The implementation demonstrates:  
- Bulk ticket classification with fallback heuristics.  
- A RAG-backed assistant that retrieves answers from ingested documentation.  
- Local persistence using Chroma DB.  
- A simple Streamlit UI for interaction.

---

## ⚙️ Features
- **Bulk Ticket Classification**: Classifies multiple tickets at once, with fallback heuristics if no OpenAI key is provided.  
- **RAG-backed Assistant**: Uses a retrieval-augmented generation flow to answer queries from ingested docs.  
- **Chroma DB Support**: Stores embeddings locally for efficient retrieval.  
- **Flexible Setup**: Works even without an OpenAI API key (heuristics only).  
- **Streamlit UI**: Simple web app interface for exploration.

---

## 🚀 Quick Start (Windows PowerShell)

1. Copy `.env.example` to `.env` and fill in `OPENAI_API_KEY` if available.  
2. Create and activate a virtual environment, then install requirements:
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
3. Confirm tickets load:

   ```powershell
   python ingest.py --list
   ```
4. *(Optional)* Fetch documentation to `data/docs`:

   ```powershell
   python ingest.py --fetch <urls>
   ```
5. Launch the Streamlit app:

   ```powershell
   streamlit run app.py
   ```

---

## 📂 Project Structure

```
.
├── app.py                  # Streamlit app (UI)
├── ingest.py               # Handles ticket/doc ingestion
├── chroma_db/              # Local Chroma DB persistence
├── data/                   # Tickets and docs folder
│   └── sample_tickets.jsonl
├── requirements.txt        # Dependencies
├── README.md               # Project documentation
└── submission.md           # Submission summary
```

---

## 🛠️ Design Decisions

1. **Fallback Heuristics :** 
   Even without an OpenAI API key, the app still classifies tickets using rule-based heuristics.

2. **Local Persistence :** 
   Chroma DB persistence ensures embeddings don’t need to be regenerated every run.

3. **Lightweight & Minimal :** 
   No heavy dependencies are used outside of `requirements.txt`, making the app easy to run locally.

---

## 🔑 Key Learnings

* Practical use of RAG (Retrieval-Augmented Generation) in a support assistant.
* Trade-offs between heuristic classification and LLM-based classification.
* Best practices for structuring AI apps with a clean, documented repo.

---

## ✅ Task Completion Status

* [✅] Added bulk ticket classification
* [✅] Integrated RAG-backed assistant with Chroma DB
* [✅] Built Streamlit UI for interaction
* [✅] Documented repo with clear setup instructions
* [ ] Future extension: Enhance UI, add advanced classification models

---

## 📜 License

This project is for **internship evaluation purposes only** under Atlan’s AI Engineer program.
If reusing this work, please ensure proper attribution and follow open-source license guidelines.


