import sqlalchemy
import pandas as pd

from config import USER, PASSWORD, HOST, DATABASE

engine = sqlalchemy.create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}")
con = engine.raw_connection()
cursor = con.cursor()

# Query example - 5 most listened artists
query = """
SELECT artist, COUNT(*) AS plays
FROM my_played_songs
GROUP BY artist
ORDER BY COUNT(*) DESC
LIMIT 5
"""

df = pd.read_sql(query, con)
print(df)
