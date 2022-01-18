import requests

from config import CLIENT_ID, URI_ENCODED, AUTHORIZATION_ENCODED, CODE, REFRESH_TOKEN


# One-time code to generate refresh_token used later in function refresh_token to generate new tokens
if __name__ == "__main__":
    # First, click on the printed url and authorize access
    request_get = "https://accounts.spotify.com/authorize?" +\
                  f"client_id={CLIENT_ID}&response_type=code&redirect_uri={URI_ENCODED}&scope=user-read-recently-played"
    print(request_get)
    # After it redirects you to your page, copy the 'code' from the url and paste it to config.py
    # Then paste the printed request to the command line (I used Git Bash):
    request = f"""curl -H 'Authorization: Basic {AUTHORIZATION_ENCODED}'""" +\
        f"""-d grant_type=authorization_code -d code={CODE}""" +\
        f"""-d redirect_uri={URI_ENCODED} https://accounts.spotify.com/api/token"""
    print(request)
    # From the response copy the refresh_token and save it in config.py


def refresh_token():
    """ Generate new token """
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "refresh_token", "refresh_token": REFRESH_TOKEN},
        headers={"Authorization": f"Basic {AUTHORIZATION_ENCODED}"}
    )

    token = response.json()["access_token"]
    return token
