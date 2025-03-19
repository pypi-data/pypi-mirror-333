import requests
from dotenv import load_dotenv
import os   
load_dotenv()
HNPBUDDY_URL = os.getenv("HNPBUDDY_URL")


def analyze_code_diff(code_diff):
    """
    Sends a code diff to the FastAPI server for analysis.
    """
    try:
        response = requests.post(
            HNPBUDDY_URL, 
            json={"code_diff": code_diff},
            headers={"Content-Type": "application/json"} 
        )
        response.raise_for_status() 
        
   
        return response.json().get("review", "No feedback received.")
    
    except requests.exceptions.RequestException as e:
        print(f"Error calling HNPBuddy API: {str(e)}")
        return "Error processing code review."
