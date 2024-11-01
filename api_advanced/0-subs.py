#!/usr/bin/python3
"""
Function to get the number of subscribers for a given subreddit.
"""
import os
import requests
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")


def number_of_subscribers(subreddit):
    """Returns the number of subscribers for a subreddit."""
    url = f"https://oauth.reddit.com/r/{subreddit}/about.json"
    auth = requests.auth.HTTPBasicAuth(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)
    headers = {"User-Agent": REDDIT_USER_AGENT}

    tokenResponse = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=auth,
        data={"grant_type": "client_credentials"},
        headers=headers
    )

    if tokenResponse.status_code == 200:
        accessToken = tokenResponse.json().get("access_token")
        headers["Authorization"] = f"bearer {accessToken}"
    else:
        print("Failed to obtain access token")
        return None

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            subscriberCount = result["data"]["subscribers"]
            return subscriberCount
        else:
            print(f"Error: Received status code {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        subreddit = sys.argv[1]
        subscribers = number_of_subscribers(subreddit)
        print(subscribers)
