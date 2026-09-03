from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(
    PROJECT_ROOT / ".env"
)


# ============================================================
# DIRECTORIES
# ============================================================

DATA_DIR = PROJECT_ROOT / "data"

DOCUMENTS_DIR = DATA_DIR / "documents"

VECTOR_DB_DIR = DATA_DIR / "vector_db"

LOG_DIR = PROJECT_ROOT / "logs"

MODELS_DIR = PROJECT_ROOT / "models"

ASSETS_DIR = PROJECT_ROOT / "assets"


for directory in [
    DATA_DIR,
    DOCUMENTS_DIR,
    VECTOR_DB_DIR,
    LOG_DIR,
    MODELS_DIR,
    ASSETS_DIR,
]:

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )


# ============================================================
# APPLICATION
# ============================================================

APP_NAME = os.getenv(
    "APP_NAME",
    "MathMind AI",
)

APP_VERSION = os.getenv(
    "APP_VERSION",
    "1.0.0",
)

DEFAULT_PROVIDER = os.getenv(
    "DEFAULT_PROVIDER",
    "Gemini",
)


# ============================================================
# LLM API KEYS
# ============================================================

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)


# ============================================================
# MODEL NAMES
# ============================================================

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-4o-mini",
)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.0-flash",
)

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile",
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2",
)


# ============================================================
# OLLAMA
# ============================================================

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434",
)


# ============================================================
# RAG CONFIGURATION
# ============================================================

CHUNK_SIZE = int(
    os.getenv(
        "CHUNK_SIZE",
        "1000",
    )
)

CHUNK_OVERLAP = int(
    os.getenv(
        "CHUNK_OVERLAP",
        "200",
    )
)

TOP_K = int(
    os.getenv(
        "TOP_K",
        "4",
    )
)

RETRIEVAL_METHOD = os.getenv(
    "RETRIEVAL_METHOD",
    "similarity",
)


# ============================================================
# CONFIDENCE
# ============================================================

HIGH_CONFIDENCE_THRESHOLD = float(
    os.getenv(
        "HIGH_CONFIDENCE_THRESHOLD",
        "0.75",
    )
)

MEDIUM_CONFIDENCE_THRESHOLD = float(
    os.getenv(
        "MEDIUM_CONFIDENCE_THRESHOLD",
        "0.45",
    )
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_api_key(
    provider: str,
) -> Optional[str]:
    """
    Return API key for the selected provider.

    Ollama does not require an API key.
    """

    provider = (
        provider.strip().lower()
    )

    if provider == "openai":

        return OPENAI_API_KEY

    if provider == "gemini":

        return GEMINI_API_KEY

    if provider == "groq":

        return GROQ_API_KEY

    if provider == "ollama":

        return None

    return None


def has_api_key(
    provider: str,
) -> bool:
    """
    Check whether the selected provider
    has a configured API key.
    """

    if provider.strip().lower() == "ollama":

        return True

    key = get_api_key(
        provider
    )

    return bool(
        key and key.strip()
    )


def get_model_name(
    provider: str,
) -> str:
    """
    Return configured model name.
    """

    provider = (
        provider.strip().lower()
    )

    if provider == "openai":

        return OPENAI_MODEL

    if provider == "gemini":

        return GEMINI_MODEL

    if provider == "groq":

        return GROQ_MODEL

    if provider == "ollama":

        return OLLAMA_MODEL

    return ""


def configuration_summary():
    """
    Return safe configuration information.

    API keys are NEVER returned.
    """

    return {
        "app_name": APP_NAME,
        "app_version": APP_VERSION,
        "default_provider": DEFAULT_PROVIDER,
        "openai_configured": has_api_key(
            "OpenAI"
        ),
        "gemini_configured": has_api_key(
            "Gemini"
        ),
        "groq_configured": has_api_key(
            "Groq"
        ),
        "ollama_configured": True,
        "openai_model": OPENAI_MODEL,
        "gemini_model": GEMINI_MODEL,
        "groq_model": GROQ_MODEL,
        "ollama_model": OLLAMA_MODEL,
        "ollama_base_url": OLLAMA_BASE_URL,
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "top_k": TOP_K,
        "retrieval_method": RETRIEVAL_METHOD,
    }