# src/config.py

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
OUTPUT_FIGURES_DIR = BASE_DIR / "outputs" / "figures"
OUTPUT_TABLES_DIR = BASE_DIR / "outputs" / "tables"

ENROLMENT_DIR = RAW_DATA_DIR / "enrolment"
BIOMETRIC_DIR = RAW_DATA_DIR / "biometric"
DEMOGRAPHIC_DIR = RAW_DATA_DIR / "demographic"

# src/config.py

# --- CREATE OUTPUT DIRECTORIES IF NOT EXIST ---
OUTPUT_FIGURES_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_TABLES_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

