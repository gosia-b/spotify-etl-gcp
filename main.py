import requests
from datetime import datetime, timedelta

from config import DATABASE_LOCATION, USER_ID, TOKEN


if __name__ == "__main__":
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }

    today = datetime.now()
    yesterday = today - timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    url = f"https://api.spotify.com/v1/me/player/recently-played?after={yesterday_unix_timestamp}"
    r = requests.get(url, headers=headers)
    data = r.json()
    print(data)
    # TODO: Convert "data" to a pandas DataFrame (import json?)
