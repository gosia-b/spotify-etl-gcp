import requests
from datetime import datetime, timedelta

import pandas as pd

from config import DATABASE_LOCATION, USER_ID, TOKEN


if __name__ == "__main__":

    # API request
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

    # Convert response: JSON to pandas DataFrame
    song_name = []
    album_name = []
    album_year = []
    artist = []
    played_at = []
    timestamp = []

    for song in data["items"]:
        song_name.append(song["track"]["name"])
        album_name.append(song["track"]["album"]["name"])
        album_year.append(song["track"]["album"]["release_date"][:4])
        artist.append(song["track"]["album"]["artists"][0]["name"])
        played_at.append(song["played_at"])
        timestamp.append(song["played_at"][:10])

    song_dict = {
        "song_name": song_name,
        "album_name": album_name,
        "album_year": album_year,
        "artist": artist,
        "played_at": played_at,
        "timestamp": timestamp
    }

    song_df = pd.DataFrame(song_dict)
    print(song_df)
