"""
One-time code to generate a token for Spotify API which doesn't expire after 1 hour
"""

import requests

from config import CLIENT_ID, URI_ENCODED, AUTHORIZATION_ENCODED, CODE, REFRESH_TOKEN

if __name__ == "__main__":
    # First, click on the printed url and authorize access
    request_get = "https://accounts.spotify.com/authorize?" +\
                  f"client_id={CLIENT_ID}&response_type=code&redirect_uri={URI_ENCODED}&scope=user-read-recently-played"
    print(request_get)

    # After it redirected me to my page, I copied the 'code' from the url and copied it to config.py
    # Now paste the printed request to the command line (I used Git Bash)
    request = f"""curl -H 'Authorization: Basic {AUTHORIZATION_ENCODED}' -d grant_type=authorization_code -d code={CODE} -d redirect_uri={URI_ENCODED} https://accounts.spotify.com/api/token"""
    print(request)
    # From the response I copied the refresh_token and saved it in config.py


def refresh_token():
    # Refresh the token
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "refresh_token", "refresh_token": REFRESH_TOKEN},
        headers={"Authorization": f"Basic {AUTHORIZATION_ENCODED}"}
    )

    token = response.json()["access_token"]
    return token
