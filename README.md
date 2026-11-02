# SentinAI — Multi-Agent Code Review and Security Auditor

SentinAI is a Streamlit application that reviews uploaded Python and JavaScript source files using local parsing, retrieval-augmented context, and three focused LLM review agents.

It produces structured JSON and a downloadable Markdown report. The health score is a deterministic triage indicator based on finding severity; it is not a certified security rating.

## Review pipeline

```text
Uploaded source files
        |
        v
Local static parsing (Python AST / Esprima)
        |
        v
Local security-reference retrieval (ChromaDB)
        |
        +---------------------+
        |          |          |
        v          v          v
    Security    Bug &       Documentation
    review      reliability review
    agent       agent       agent
        |          |          |
        +----------+----------+
                   |
                   v
        Structured report builder
                   |
             JSON + Markdown
```

## Capabilities

- Python parsing with the built-in AST module.
- JavaScript parsing through Esprima and Node.js.
- Separate security, reliability/bug, and documentation review agents.
- Retrieval of relevant local references from a ChromaDB collection.
- Structured findings with severity and file attribution.
- Markdown report and JSON output.
- Groq as the default LLM provider, with optional OpenAI configuration and fallback.

## Technology stack

Python, Streamlit, LangGraph, LangChain, Groq, OpenAI (optional), ChromaDB, Sentence Transformers, Python AST, Esprima, Node.js, and Docker.

## Requirements

- Python 3.11+
- Node.js and npm (required for JavaScript parsing)
- A Groq API key, or an OpenAI API key with the provider configured
- Internet access on first run if the embedding model needs to be downloaded

## Local setup

1. Clone the repository and enter the project directory.
2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   # Windows PowerShell
   .\.venv\Scripts\Activate.ps1
   # macOS / Linux
   source .venv/bin/activate
   ```

3. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Install the JavaScript parser dependency:

   ```bash
   npm ci
   ```

5. Configure local environment variables:

   ```bash
   # Windows PowerShell
   Copy-Item .env.example .env
   # macOS / Linux
   cp .env.example .env
   ```

   Set `GROQ_API_KEY`. For OpenAI, set `SENTINAI_LLM_PROVIDER=openai` and `OPENAI_API_KEY`.

6. Start the application:

   ```bash
   streamlit run app.py
   ```

## Docker

```bash
docker build -t sentinai .
docker run --rm -p 8501:8501 --env-file .env sentinai
```

Open `http://localhost:8501`.

## Repository layout

- `app.py` — Streamlit interface and report presentation
- `sentinai/agents.py` — LangGraph workflow and specialist agents
- `sentinai/core.py` — application orchestration and RAG retrieval
- `sentinai/parsers.py` — local Python and JavaScript parsing
- `sentinai/rag.py` — local reference indexing and retrieval
- `sentinai/prompts.py` — specialist review instructions
- `sentinai/data/references.json` — curated local reference data
- `tests/` — automated unit tests

## Tests

Run the unit tests with:

```bash
pytest -q
```

The tests cover response parsing, deterministic severity scoring, and local parser behavior. They do not make live LLM calls.

## Important limitations

- LLM findings can be incomplete or incorrect; manually validate important results.
- Static parsing is not a full program analysis and does not execute uploaded code.
- RAG uses the local reference set in this repository; it is not a live vulnerability database.
- The health score is a transparent severity-penalty summary, not a formal quality or compliance score.
- Uploaded code is sent to the configured LLM provider. Do not upload confidential source code unless authorized.
- This tool does not replace a professional penetration test, SAST platform, or human security review.

## Security

Keep API keys in `.env` or a managed secret store. Never commit populated environment files, API tokens, private keys, or proprietary source code.
