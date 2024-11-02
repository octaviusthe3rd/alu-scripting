#!/usr/bin/python3
"""
This script retrieves the titles of the first 10 hot posts for a given subreddit using the Reddit API.
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

def top_ten(subreddit):
    """
    Prints the titles of the first 10 hot posts for a given subreddit.
    
    Args:
        subreddit (str): The name of the subreddit to check.
    
    Returns:
        None: Prints the titles or None if subreddit is invalid
    """
    url = f"https://oauth.reddit.com/r/{subreddit}/hot.json?limit=10"
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
        
        # Fetch hot posts
        response = requests.get(url, headers=headers, allow_redirects=False)
        
        # Check for redirect (invalid subreddit)
        if response.status_code == 302:
            print(None)
            return
        
        response.raise_for_status()
        
        # Parse and print post titles
        posts = response.json().get("data", {}).get("children", [])
        if not posts:
            print(None)
            return
            
        for post in posts:
            print(post["data"]["title"])
            
    except requests.exceptions.HTTPError:
        print(None)
    except Exception as e:
        print(None)

if __name__ == "__main__":
    """
    Main function to handle command-line argument and display hot posts.
    """
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        top_ten(sys.argv[1])
