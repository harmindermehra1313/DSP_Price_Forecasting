import pandas as pd

def compute_lags(df):
    """
    Adds lag features for india_price.
    Matches GRU training notebook exactly.
    """
    lags = [2, 4, 5, 9, 18, 24]

    for l in lags:
        df[f"lag_{l}"] = df["india_price"].shift(l)

    return df