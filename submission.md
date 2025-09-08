Project: **Customer Support Copilot**  
Author: Boddu Lakshmi Narayana Gupta (AI Engineer Intern)

## What I submitted
- Streamlit app: `app.py` (dashboard + assistant)
- Ingest helper: `ingest.py` (loads tickets + can fetch docs)
- Local DB: `chroma_db/` (Chroma local persistence)
- Sample tickets/docs: `data/`
- Requirements: `requirements.txt`
- Documentation: `README.md`, `submission.md`

## How to run
- See [README.md](./README.md) for detailed setup instructions.
- Basic demo steps:  
  1. Run `python ingest.py --list`  
  2. Launch with `streamlit run app.py`

## Notes / Next Steps
- (Future improvement) Add more docs to improve RAG answers.
- (Future improvement) Tweak classifier heuristics or integrate OpenAI API for better results.
