import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_BASE_URL")

if not API_URL:
    raise ValueError(
        "❌ API_BASE_URL is not set! Please add it to your environment variables."
    )
