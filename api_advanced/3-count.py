#!/usr/bin/python3
"""
Python Script for Reddit API word counting in hot posts
"""
import os
import sys
import requests
from dotenv import load_dotenv


def count_words(subreddit, word_list, after=None, word_count=None):
    """
    Count occurrences of words in subreddit's hot post titles
    """
    # Initialize word_count on first call
    if word_count is None:
        word_count = {}

    # Load environment variables
    load_dotenv()
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT")

    # Setup auth and headers
    url = "https://oauth.reddit.com/r/{}/hot".format(subreddit)
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    headers = {'User-Agent': user_agent}

    try:
        # Get access token
        token_res = requests.post(
            "https://www.reddit.com/api/v1/access_token",
            auth=auth,
            data={"grant_type": "client_credentials"},
            headers=headers
        )
        if token_res.status_code != 200:
            return None

        # Update headers with token
        access_token = token_res.json().get("access_token")
        headers["Authorization"] = "bearer {}".format(access_token)

        # Get subreddit posts
        params = {'limit': 100}
        if after:
            params['after'] = after

        response = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False
        )
        if response.status_code != 200:
            return None

        # Process posts
        data = response.json().get('data')
        posts = data.get('children')
        
        for post in posts:
            title = post['data']['title']
            for word in word_list:
                if word.lower() in title.lower():
                    word_count[word.lower()] = word_count.get(word.lower(), 0) + 1

        # Get next page token
        after = data.get('after')

        # If there's a next page, recurse
        if after:
            return count_words(subreddit, word_list, after, word_count)
        # If no next page, print results and return
        elif word_count:
            for key, value in sorted(word_count.items(),
                                   key=lambda x: (-x[1], x[0])):
                print("{}: {}".format(key.lower(), value))
            return
        return None

    except Exception as e:
        return None


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programming 'python java javascript'".format(sys.argv[0]))
    else:
        count_words(sys.argv[1], [x for x in sys.argv[2].split()])
