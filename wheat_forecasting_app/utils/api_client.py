import requests
from config.api_keys import FRED_API_KEY

FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

def fetch_fred_latest(series_id: str):
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
    }

    try:
        resp = requests.get(FRED_BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        observations = data.get("observations", [])
        # walk backwards to find last valid value
        for row in reversed(observations):
            val = row.get("value")
            if val not in (None, ".", ""):
                return float(val)
    except Exception:
        return None

    return None