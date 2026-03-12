def compute_rolling(df):
    """
    Rolling means: roll3, roll6, roll12
    """
    df["roll3"] = df["india_price"].rolling(3).mean()
    df["roll6"] = df["india_price"].rolling(6).mean()
    df["roll12"] = df["india_price"].rolling(12).mean()
    return df