"""Runtime configuration, read from environment variables."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:***REMOVED***@localhost/api_db")
MODELS_DIR = Path(os.getenv("MODELS_DIR", ROOT / "models"))
CORS_ORIGINS = [
    o.strip()
    for o in os.getenv(
        "CORS_ORIGINS", "http://127.0.0.1:5500,http://localhost:5500,http://localhost"
    ).split(",")
    if o.strip()
]
