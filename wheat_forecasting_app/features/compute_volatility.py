def compute_volatility(df):
    """
    Volatility features: vol3, vol6
    """
    returns = df["india_price"].pct_change()

    df["vol3"] = returns.rolling(3).std()
    df["vol6"] = returns.rolling(6).std()

    return df