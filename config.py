import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
VECTOR_DB_DIR = DATA_DIR / "vector_db"

MODELS_DIR = BASE_DIR / "models"

LOGS_DIR = BASE_DIR / "logs"

ASSETS_DIR = BASE_DIR / "assets"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

DEFAULT_MODEL = os.getenv(
    "DEFAULT_MODEL",
    "gpt-4.1-mini",
)

APP_NAME = "MathMind AI"

APP_VERSION = "1.0.0"

DEBUG = True