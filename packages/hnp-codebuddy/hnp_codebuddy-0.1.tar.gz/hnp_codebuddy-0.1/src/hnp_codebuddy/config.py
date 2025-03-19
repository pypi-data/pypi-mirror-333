import os
from dotenv import load_dotenv

load_dotenv()

HNPBUDDY_URL = os.getenv("HNPBUDDY_URL", "http://10.80.20.162:5000/review")
