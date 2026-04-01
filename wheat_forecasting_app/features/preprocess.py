
import pandas as pd

def preprocess_raw_data(master_path, live_dict):
    """
    Load master_monthly.parquet and inject scenario values
    ONLY into the last row, without altering historical prices.
    """
    df = pd.read_parquet(master_path)

    df["month"] = pd.to_datetime(df["month"])
    df = df.set_index("month")

    # Fix only non-price NaNs
    for col in ["rainfall", "temperature"]:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].mean())

    # Compute return if missing
    if "return" not in df.columns:
        df["return"] = df["india_price"].pct_change()

    # Drop rows where india_price is missing
    df = df.dropna(subset=["india_price"])

    # Identify the TRUE last month
    last_idx = df.index[-1]

    # Inject scenario values ONLY into last row
    for key, value in live_dict.items():
        if key in df.columns and key != "india_price":
            df.loc[last_idx, key] = value

    # Do NOT ffill/bfill entire dataframe
    # Only fill missing scenario values in last row if needed
    df.loc[last_idx] = df.loc[last_idx].fillna(method="ffill")

    return df
