import requests
from dotenv import load_dotenv
import os


load_dotenv()


BASE_URL = "https://api.bitbucket.org/2.0"
AUTH = (os.getenv("BITBUCKET_USERNAME"), os.getenv("BITBUCKET_APP_PASSWORD"))
BITBUCKET_WORKSPACE = os.getenv("BITBUCKET_WORKSPACE")
BITBUCKET_REPO = os.getenv("BITBUCKET_REPO")

def fetch_pull_requests():
    """Fetch all open pull requests."""
    url = f"{BASE_URL}/repositories/{BITBUCKET_WORKSPACE}/{BITBUCKET_REPO}/pullrequests"
    response = requests.get(url, auth=AUTH)
    if response.status_code == 200:
        return response.json().get("values", [])
    else:
        raise Exception(f"Failed to fetch PRs: {response.status_code}, {response.text}")

def fetch_diff(pr_id):
    """Fetch the code diff for a specific pull request."""
    url = f"{BASE_URL}/repositories/{BITBUCKET_WORKSPACE}/{BITBUCKET_REPO}/pullrequests/{pr_id}/diff"
    response = requests.get(url, auth=AUTH)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch diff for PR #{pr_id}: {response.status_code}, {response.text}")

def post_comment(pr_id, message):
    """Post a comment on a pull request."""
    url = f"{BASE_URL}/repositories/{BITBUCKET_WORKSPACE}/{BITBUCKET_REPO}/pullrequests/{pr_id}/comments"
    payload = {"content": {"raw": message}}
    response = requests.post(url, json=payload, auth=AUTH)
    if response.status_code == 201:
        print(f"Successfully comment posted on PR #{pr_id}: {message}")
    else:
        raise Exception(f"Failed to post comment: {response.status_code}, {response.text}")
