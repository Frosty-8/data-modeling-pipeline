from fastapi import FastAPI
import joblib
import pandas as pd

from src.feature_engineering.feature_builder import FeatureBuilder

app = FastAPI()

# Load model once
from config.paths import MODEL_PATH
model = joblib.load(MODEL_PATH)


@app.get("/health")
def health():
    return {"status": "ok"}

EXPECTED_COLUMNS = model.feature_names_in_

@app.post("/predict")
def predict(data: dict):
    df = pd.DataFrame([data])

    # ✅ FIX: convert Join_Date
    df["Join_Date"] = pd.to_datetime(df["Join_Date"], errors="coerce")

    builder = FeatureBuilder(df)
    X = builder.create_features().encode().get_data()

    X = X.reindex(columns=EXPECTED_COLUMNS, fill_value=0)

    prediction = model.predict(X)[0]

    return {"prediction": prediction}