from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

from model.load_model import load_all
from model.predict import GRUPredictor
from features.preprocess import preprocess_raw_data
from features.feature_pipeline import build_feature_pipeline

MASTER_PATH = "data/historical/master_monthly.parquet"

# Load model + scalers once
model, feature_scaler, target_scaler, feature_columns = load_all()

# Load master dataset once
df_master = pd.read_parquet(MASTER_PATH)
df_master["month"] = pd.to_datetime(df_master["month"])
df_master = df_master.set_index("month")

# Fix NaN using seasonal averages
df_master["rainfall"] = df_master["rainfall"].fillna(
    df_master["rainfall"].groupby(df_master.index.month).transform("mean")
)
df_master["temperature"] = df_master["temperature"].fillna(
    df_master["temperature"].groupby(df_master.index.month).transform("mean")
)

app = FastAPI()

class Scenario(BaseModel):
    oil_price: float
    usd_inr: float
    rainfall: float
    conflict_events: float
    fertiliser_index: float
    temperature: float

@app.post("/predict")
def predict_price(scenario: Scenario):

    live_dict = {
        "oil_price": scenario.oil_price,
        "usd_inr": scenario.usd_inr,
        "rainfall": scenario.rainfall,
        "conflict_events": scenario.conflict_events,
        "fertiliser_index": scenario.fertiliser_index,
        "temperature": scenario.temperature,

        # untouched features
        "gepu": df_master.iloc[-1]["gepu"],
        "global_wheat_price": df_master.iloc[-1]["global_wheat_price"],
        "fao_cereals": df_master.iloc[-1]["fao_cereals"],
    }

    df_raw = preprocess_raw_data(MASTER_PATH, live_dict)
    df_features = build_feature_pipeline(df_raw)

    predictor = GRUPredictor(model, feature_scaler, target_scaler, feature_columns)
    result = predictor.predict(df_features)

    return {
        "predicted_price": float(result["predicted_price"]),
        "predicted_return": float(result["predicted_return"])
    }