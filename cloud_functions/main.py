import logging
import requests
from datetime import datetime, timedelta

import pandas as pd
from dateutil import parser
import sqlalchemy

from validation import check_if_valid_data
from refresh_token import refresh_token
from config import USER, PASSWORD, HOST, DATABASE


def main_function(event, context) -> None:
    logging.basicConfig(level=logging.INFO)
    token = refresh_token()

    # API request
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    now = datetime.now()
    yesterday = now - timedelta(days=2)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    url = f"https://api.spotify.com/v1/me/player/recently-played?after={yesterday_unix_timestamp}"
    r = requests.get(url, headers=headers)
    data = r.json()

    # Convert response: JSON to pandas DataFrame
    played_at = []
    song_name = []
    artist = []
    album_name = []
    album_year = []

    for song in data["items"]:
        played_at.append(parser.parse(song["played_at"]))
        song_name.append(song["track"]["name"])
        artist.append(song["track"]["album"]["artists"][0]["name"])
        album_name.append(song["track"]["album"]["name"])
        album_year.append(song["track"]["album"]["release_date"][:4])

    song_dict = {
        "played_at": played_at,
        "song_name": song_name,
        "artist": artist,
        "album_name": album_name,
        "album_year": album_year
    }

    song_df = pd.DataFrame(song_dict)
    logging.info("Data extracted from Spotify API")

    # Validate
    if check_if_valid_data(song_df):
        logging.info("Data valid, proceed to load stage")

        # Connect to the database
        engine = sqlalchemy.create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}")
        con = engine.raw_connection()
        cursor = con.cursor()
        logging.info("Opened database successfully")

        # Create table
        query_create_table = """
        CREATE TABLE IF NOT EXISTS my_played_songs(
            played_at TIMESTAMP,
            song_name VARCHAR(200),
            artist VARCHAR(200),
            album_name VARCHAR(200),
            album_year INT(4),
            CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
        )
        """
        cursor.execute(query_create_table)
        logging.info("Table created or already exists")

        # Append dataframe to the database table
        for i, _ in song_df.iterrows():
            try:
                song_df.iloc[i:i+1].to_sql("my_played_songs", con=engine, index=False, if_exists="append")
            except sqlalchemy.exc.IntegrityError:
                pass  # If played_at already exists in the table, don't insert the row
