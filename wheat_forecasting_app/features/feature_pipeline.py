import pandas as pd

def build_feature_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Ensure datetime index
    if not isinstance(df.index, pd.DatetimeIndex):
        df["month"] = pd.to_datetime(df["month"])
        df = df.set_index("month")

    # 1. Base return
    if "return" not in df.columns:
        df["return"] = df["india_price"].pct_change()

    # 2. Lags on india_price (exact names from feature_columns.json)
    df["lag_2"] = df["india_price"].shift(2)
    df["lag_4"] = df["india_price"].shift(4)
    df["lag_5"] = df["india_price"].shift(5)
    df["lag_9"] = df["india_price"].shift(9)
    df["lag_18"] = df["india_price"].shift(18)
    df["lag_24"] = df["india_price"].shift(24)

    # 3. Rolling means
    df["roll3"] = df["india_price"].rolling(3).mean()
    df["roll6"] = df["india_price"].rolling(6).mean()
    df["roll12"] = df["india_price"].rolling(12).mean()

    # 4. Volatility
    df["vol3"] = df["india_price"].rolling(3).std()
    df["vol6"] = df["india_price"].rolling(6).std()

    # 5. Momentum
    df["mom1"] = df["india_price"].pct_change(1)
    df["mom3"] = df["india_price"].pct_change(3)
    df["mom6"] = df["india_price"].pct_change(6)

    # 6. Rolling min/max
    df["roll_min_6"] = df["india_price"].rolling(6).min()
    df["roll_max_6"] = df["india_price"].rolling(6).max()

    # 7. Month dummies (2–12)
    df["month_num"] = df.index.month
    month_dummies = pd.get_dummies(df["month_num"], prefix="month_num")

    for m in range(2, 13):
        col = f"month_num_{m}"
        if col not in month_dummies.columns:
            month_dummies[col] = 0

    df = pd.concat([df, month_dummies], axis=1)

    # 8. Fill NaNs so last row is valid
    df = df.ffill().bfill()

    return df