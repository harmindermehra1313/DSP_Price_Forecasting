import json
from pathlib import Path

import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

from features.feature_pipeline import build_feature_pipeline

BASE = Path(__file__).resolve().parent
MASTER_PATH = BASE.parent / "data" / "historical" / "master_monthly.parquet"


def load_all():
    # 1. Load GRU model
    model_path = BASE / "gru_model_20260310_194421.keras"
    model = tf.keras.models.load_model(model_path, compile=False)

    # 2. Load feature column names from training (36 features)
    with open(BASE / "feature_columns.json", "r") as f:
        feature_columns = json.load(f)

    # 3. Load master data
    df = pd.read_parquet(MASTER_PATH)
    df["month"] = pd.to_datetime(df["month"])
    df = df.set_index("month")

    if "return" not in df.columns:
        df["return"] = df["india_price"].pct_change()

    df = df.dropna(subset=["return"])

    # 4. Build engineered features
    df_features = build_feature_pipeline(df.copy())

    # 5. Ensure all training features exist
    missing = [c for c in feature_columns if c not in df_features.columns]
    if missing:
        raise ValueError(f"Missing features in pipeline output: {missing}")

    X = df_features[feature_columns]

    # 6. Fit scalers
    feature_scaler = MinMaxScaler()
    feature_scaler.fit(X)

    target_scaler = MinMaxScaler()
    target_scaler.fit(df[["return"]])

    return model, feature_scaler, target_scaler, feature_columns