import os
from dotenv import load_dotenv

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
SENTINAI_LLM_PROVIDER = os.getenv("SENTINAI_LLM_PROVIDER", "groq").strip().lower()
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "./chromadb").strip()
DEFAULT_MODEL = os.getenv("SENTINAI_LLM_MODEL", "llama-3.3-70b-versatile").strip()
OPENAI_DEFAULT_MODEL = os.getenv("SENTINAI_OPENAI_MODEL", "gpt-4o-mini").strip()
EMBEDDING_MODEL = os.getenv("SENTINAI_EMBEDDING_MODEL", "all-MiniLM-L6-v2").strip()
FALLBACK_TO_OPENAI = os.getenv("SENTINAI_FALLBACK_TO_OPENAI", "false").strip().lower() in ("1", "true", "yes")

if SENTINAI_LLM_PROVIDER == "groq" and not GROQ_API_KEY and not OPENAI_API_KEY:
    raise EnvironmentError(
        "GROQ_API_KEY is required when SENTINAI_LLM_PROVIDER is set to groq unless OPENAI_API_KEY is provided for fallback."
    )

if SENTINAI_LLM_PROVIDER == "openai" and not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY is required when SENTINAI_LLM_PROVIDER is set to openai.")
