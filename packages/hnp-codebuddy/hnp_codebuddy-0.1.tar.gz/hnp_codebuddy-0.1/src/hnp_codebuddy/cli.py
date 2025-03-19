from hnp_codebuddy.bitbucket import fetch_pull_requests, fetch_diff, post_comment
from hnp_codebuddy.api_client import analyze_code_diff


def review_pr():
    """Review all open pull requests."""
    print("Fetching open PRs...")
    pull_requests = fetch_pull_requests()

    if not pull_requests:
        print("No open pull requests found.")
        return

    for pr in pull_requests:
        print(f"Reviewing the following PR #{pr['id']}: {pr['title']}")
        try:
            diff = fetch_diff(pr["id"])
            feedback = analyze_code_diff(diff)
            post_comment(pr["id"], feedback)
        except Exception as e:
            print(f"Error processing PR #{pr['id']}: {e}")

if __name__ == "__main__":
    review_pr()
