import requests

from config import REFRESH_TOKEN, AUTHORIZATION_ENCODED


def refresh_token() -> str:
    """ Generate new token """
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "refresh_token", "refresh_token": REFRESH_TOKEN},
        headers={"Authorization": f"Basic {AUTHORIZATION_ENCODED}"}
    )

    token = response.json()["access_token"]
    return token
