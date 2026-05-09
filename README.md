# SentinAI

SentinAI is a multi-agent Retrieval-Augmented Generation platform for automated code review, security auditing, and documentation generation for Python and JavaScript.

## Setup

1. Create a Python virtual environment and activate it.
2. Install dependencies:

```powershell
pip install -r requirements.txt
npm install
```

3. Copy `.env.example` to `.env` and set your API key.

```powershell
copy .env.example .env
```

4. Update `.env` with your Groq API key:

```powershell
GROQ_API_KEY=YOUR_GROQ_API_KEY
SENTINAI_LLM_PROVIDER=groq
SENTINAI_LLM_MODEL=llama-3.3-70b-versatile
```

5. Run the Streamlit app:

```powershell
streamlit run app.py
```

## Docker Deployment

Build and run locally with Docker:

```powershell
docker build -t sentinai .
docker run --rm -p 8501:8501 --env-file .env sentinai
```

Or use Docker Compose:

```powershell
$env:GROQ_API_KEY="YOUR_GROQ_API_KEY"
docker compose up --build
```

## Notes

- The system uses Python AST for Python analysis.
- It uses Esprima for JavaScript parsing through Node.js.
- Vector retrieval uses ChromaDB with sentence-transformer embeddings.
- The default LLM provider is now Groq, with OpenAI as an optional fallback.
