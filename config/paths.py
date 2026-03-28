from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"
RAW_DATA_PATH = DATA_DIR / "raw" / "raw_data.csv"
PROCESSED_DATA_PATH = DATA_DIR / "processed" / "cleaned_data.csv"
CONFIG_PATH = BASE_DIR / "config" / "config.yaml"

DB_PATH = DATA_DIR / "pipeline.db"

ARTIFACTS_DIR = BASE_DIR / "artifacts"
MODEL_PATH = ARTIFACTS_DIR / "model.pkl"