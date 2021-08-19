import requests
import twitter_secrets

bearer_token = twitter_secrets.secrets.get('Bearer Token')
search_url = "https://api.twitter.com/2/tweets/search/recent"
cols_names = ['author_id', 'id', 'text']

def bearer_oauth(bear):
    """
    Method required by bearer token authentication.
    """

    bear.headers["Authorization"] = f"Bearer {bearer_token}"
    bear.headers["User-Agent"] = "v2RecentSearchPython"
    return bear


def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()
