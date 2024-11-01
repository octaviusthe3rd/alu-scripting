#!/usr/bin/python3
"""
Module to retrieve and print the titles of the first 10 hot posts from a subreddit.
"""

import os
import requests
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

def top_ten(subreddit):
    """
    Queries the Reddit API to print the titles of the top 10 hot posts for a given subreddit.

    Args:
        subreddit (str): The name of the subreddit to query.
        
    Returns:
        None
    """
    url = f"https://oauth.reddit.com/r/{subreddit}/hot"
    auth = requests.auth.HTTPBasicAuth(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)
    headers = {"User-Agent": REDDIT_USER_AGENT}

    try:
        # Obtain access token
        token_response = requests.post(
            "https://www.reddit.com/api/v1/access_token",
            auth=auth,
            data={"grant_type": "client_credentials"},
            headers=headers
        )
        token_response.raise_for_status()
        
        # Get access token and add to headers
        access_token = token_response.json().get("access_token")
        headers["Authorization"] = f"bearer {access_token}"

        # Query the subreddit for top 10 hot posts
        response = requests.get(url, headers=headers, params={"limit": 10}, allow_redirects=False)
        
        # Check for valid subreddit
        if response.status_code == 200:
            posts = response.json().get("data", {}).get("children", [])
            for post in posts:
                print(post["data"]["title"])
        else:
            print(None)

    except Exception as e:
        print(None)

