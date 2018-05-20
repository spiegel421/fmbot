import mysql.connector
import time
from mysql.connector import errorcode

DB_NAME = 'scrobbles'
NUM_DAYS = 1

cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
cursor = cnx.cursor()

time_cap = str(time.time() - 86400 * NUM_DAYS)

select_artists = ("SELECT artist FROM scrobbles "
                  "WHERE timestamp > " + time_cap)

cursor.execute(select_artists)

trending_artist_dict = {}
for artist in cursor:
    if artist in trending_artist_dict:
        trending_artist_dict[artist] += 1
    else:
        trending_artist_dict[artist] = 1

cnx.commit()
cursor.close()
cnx.close()


print(trending_artist_dict)
