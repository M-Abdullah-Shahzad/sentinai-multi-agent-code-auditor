import os

from dotenv import load_dotenv

# Real process environment variables take precedence over local .env values.
load_dotenv(override=False)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
SENTINAI_LLM_PROVIDER = os.getenv("SENTINAI_LLM_PROVIDER", "groq").strip().lower()
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "./chromadb").strip()
DEFAULT_MODEL = os.getenv("SENTINAI_LLM_MODEL", "llama-3.3-70b-versatile").strip()
OPENAI_DEFAULT_MODEL = os.getenv("SENTINAI_OPENAI_MODEL", "gpt-4o-mini").strip()
EMBEDDING_MODEL = os.getenv("SENTINAI_EMBEDDING_MODEL", "all-MiniLM-L6-v2").strip()
FALLBACK_TO_OPENAI = os.getenv("SENTINAI_FALLBACK_TO_OPENAI", "false").strip().lower() in ("1", "true", "yes")
