import mysql.connector
import time
from mysql.connector import errorcode

def find_trending_artists(num_days):
    DB_NAME = 'scrobbles'

    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor()

    time_cap = str(time.time() - 86400 * num_days)

    select_artists = ("SELECT artist FROM scrobbles "
                      "WHERE timestamp > " + time_cap)

    cursor.execute(select_artists)

    trending_artist_dict = {}
    for artist in cursor:
        if artist[0] in trending_artist_dict:
            trending_artist_dict[artist[0]] += 1
        else:
            trending_artist_dict[artist[0]] = 1

    cnx.commit()
    cursor.close()
    cnx.close()

    return trending_artist_dict
