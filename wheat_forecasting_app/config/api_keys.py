import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Read API keys from environment variables
FRED_API_KEY = os.getenv("FRED_API_KEY")

if not FRED_API_KEY:
    raise ValueError("FRED_API_KEY is missing. Add it to your .env file.")