
import pandas as pd

# def preprocess_raw_data(master_path, live_dict):
#     """
#     Load master_monthly.parquet and inject scenario values
#     into the LAST ROW only.
#     """
#     df = pd.read_parquet(master_path)

#     df["month"] = pd.to_datetime(df["month"])
#     df = df.set_index("month")

#     if "return" not in df.columns:
#         df["return"] = df["india_price"].pct_change()

#     df = df.dropna(subset=["return"])

#     df = df.copy()
#     for key, value in live_dict.items():
#         if key in df.columns:
#             df.iloc[-1, df.columns.get_loc(key)] = value

#     df = df.ffill().bfill()

#     return df

def preprocess_raw_data(master_path, live_dict):
    """
    Load master_monthly.parquet and inject scenario values
    into the LAST ROW only.
    """
    df = pd.read_parquet(master_path)

    df["month"] = pd.to_datetime(df["month"])
    df = df.set_index("month")

    # FIX NAN VALUES IN IMPORTANT COLUMNS
    df["rainfall"] = df["rainfall"].fillna(df["rainfall"].mean())
    df["temperature"] = df["temperature"].fillna(df["temperature"].mean())

    if "return" not in df.columns:
        df["return"] = df["india_price"].pct_change()

    df = df.dropna(subset=["return"])

    # Inject scenario values into last row
    df = df.copy()
    for key, value in live_dict.items():
        if key in df.columns:
            df.iloc[-1, df.columns.get_loc(key)] = value

    # Final cleanup
    df = df.ffill().bfill()

    return df

# def preprocess_raw_data(master_path, live_dict):
#     """
#     Load master_monthly.parquet and inject scenario values
#     into the LAST ROW only.
#     """
#     df = pd.read_parquet(master_path)

#     df["month"] = pd.to_datetime(df["month"])
#     df = df.set_index("month")

#     # FIX NAN VALUES USING SEASONAL AVERAGES
#     df["rainfall"] = df["rainfall"].fillna(
#         df["rainfall"].groupby(df.index.month).transform("mean")
#     )

#     df["temperature"] = df["temperature"].fillna(
#         df["temperature"].groupby(df.index.month).transform("mean")
#     )

#     if "return" not in df.columns:
#         df["return"] = df["india_price"].pct_change()

#     df = df.dropna(subset=["return"])

#     # Inject scenario values into last row
#     df = df.copy()
#     for key, value in live_dict.items():
#         if key in df.columns:
#             df.iloc[-1, df.columns.get_loc(key)] = value

#     # Final cleanup
#     df = df.ffill().bfill()

#     return df