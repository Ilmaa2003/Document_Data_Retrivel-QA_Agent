
# AI Agent: Document Q&A / Info Retrieval

<img width="1527" height="633" alt="Screenshot 2025-11-25 025418" src="https://github.com/user-attachments/assets/a04c1f04-bb55-428f-abd5-dd75e58c7bf7" />

<img width="1919" height="854" alt="image" src="https://github.com/user-attachments/assets/24333112-4d74-4ae9-8fe4-3686ba7c613f" />


## Project Overview
This project implements an AI-powered agent designed to provide accurate answers from uploaded documents (PDFs). It converts unstructured document content into structured, actionable responses and supports multi-turn queries.

**Target Users:**
- Employees, students, or professionals needing instant document insights.
- Users without technical expertise.

**Problems Solved:**
- Manual document searching is time-consuming.
- Allows contextual Q&A over PDFs.
- Supports multi-turn conversations for follow-up queries.

---

## Features
- Upload PDF documents for indexing.
- Interactive chat interface for querying documents.
- Multi-turn conversational support.
- Vector search for fast and accurate information retrieval.
- Prototype workflow using n8n, Pinecone embeddings, Gemini LLM, and Streamlit.

---

## System Architecture

| Component        | Tool Used       | Purpose                                                      |
|-----------------|----------------|--------------------------------------------------------------|
| AI Engine / LLM | Gemini         | Generate answers based on retrieved document context        |
| Workflow Builder | n8n            | Automate document indexing, vector search, and LLM query   |
| Data Source      | PDF files       | Provide documents for Q&A                                    |
| Interface / Chat UI | Streamlit   | Interactive chat interface for users                        |
| Embedding Store  | Pinecone       | Store document embeddings for retrieval                      |

**Workflow Steps (Simplified):**
1. User uploads a PDF via Streamlit UI.
2. PDF is processed, and embeddings are stored in Pinecone.
3. User queries the document through chat.
4. n8n workflow performs vector search in Pinecone.
5. Gemini LLM generates responses based on retrieved context.
6. Response is returned to the user in the chat interface.

---

## Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 20+ (for n8n)
- Pinecone account and API key
- Gemini LLM API access
- `pip` and `npm` installed

### Backend / AI Agent Setup
1. Clone the repository:
```bash
git clone <repo-url>
cd <repo-folder>
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Set environment variables:
```bash
export PINECONE_API_KEY="your_pinecone_api_key"
export GEMINI_API_KEY="your_gemini_api_key"
export PINECONE_ENVIRONMENT="your_pinecone_env"
```

---

### n8n Workflow Setup
1. Install n8n globally:
```bash
npm install -g n8n
```

2. Start n8n:
```bash
n8n
```

3. Import the workflow file (`workflow.json`) into n8n.
4. Configure nodes for:
   - PDF ingestion
   - Pinecone embedding insertion
   - LLM query execution
5. Activate workflow.

---

### Streamlit UI Setup
1. Run Streamlit app:
```bash
streamlit run app.py
```

2. Open browser at `http://localhost:8501`.
3. Upload a PDF and start asking questions.

---

## Future Enhancements
- Support multiple PDFs simultaneously.
- Richer UI/UX with better conversation history.
- Advanced query handling and analytics logging.
- Role-based authentication for enterprise use.

---

## Summary
This prototype integrates the core components (Streamlit UI, n8n workflow, Gemini LLM, Pinecone embeddings) to index PDFs, perform vector search, and generate accurate, contextual responses. It provides a foundation for a fully-featured AI document assistant.
