#!/usr/bin/python3
"""
This script retrieves the number of subscribers for a given subreddit using the Reddit API.
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
    """
    Returns the number of subscribers for a subreddit.
    
    Args:
        subreddit (str): The name of the subreddit to check.
        
    Returns:
        int or None: The number of subscribers if successful, None otherwise.
    """
    url = f"https://oauth.reddit.com/r/{subreddit}/about.json"
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

        # Get access token
        access_token = token_response.json().get("access_token")
        headers["Authorization"] = f"bearer {access_token}"

        # Fetch subreddit information
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        result = response.json()
        subscriber_count = result["data"]["subscribers"]
        return subscriber_count

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print(f"Error: Subreddit '{subreddit}' does not exist.")
        else:
            print(f"Error: HTTP error occurred: {http_err}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    """
    Main function to handle command-line argument and display subscriber count.
    """
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        subreddit = sys.argv[1]
        subscribers = number_of_subscribers(subreddit)
        if subscribers is not None:
            print(f"Subscribers in '{subreddit}': {subscribers:,}")
        else:
            print(f"Unable to retrieve subscriber count for '{subreddit}'.")
