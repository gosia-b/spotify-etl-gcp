import pandas as pd
import sqlalchemy

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

# Connect to the database
engine = sqlalchemy.create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}")
con = engine.raw_connection()
cursor = con.cursor()

# Create table
cursor.execute(query_create_table)

# Show all tables in the database
df = pd.read_sql(query_show_tables, engine)
print(df)
