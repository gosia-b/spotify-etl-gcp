import logging
import requests
from datetime import datetime, timedelta

import pandas as pd
from dateutil import parser

from config import DATABASE_LOCATION, USER_ID, TOKEN
from validation import check_if_valid_data


if __name__ == "__main__":

    # API request
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }

    now = datetime.now()
    yesterday = now - timedelta(days=1)
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
        played_at.append(parser.parse(song["played_at"]))

    song_dict = {
        "song_name": song_name,
        "album_name": album_name,
        "album_year": album_year,
        "artist": artist,
        "played_at": played_at
    }

    song_df = pd.DataFrame(song_dict)
    print(song_df)

    logging.info("Data extracted")

    # Validate
    if check_if_valid_data(song_df):
        logging.info("Data valid, proceed to load stage")
