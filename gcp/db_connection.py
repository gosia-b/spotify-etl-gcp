import pandas as pd
import mysql.connector

from db_credentials import USER, PASSWORD, HOST, DATABASE


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

query_show_tables = """
SHOW TABLES
"""

with mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE) as con:
    # Create table
    cursor = con.cursor()
    cursor.execute(query_create_table)

    # Show all tables in the database
    df = pd.read_sql(query_show_tables, con)
    print(df)
