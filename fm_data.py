import mysql.connector
from mysql.connector import errorcode
import time

DB_NAME = 'scrobbles'

TABLES = {}
TABLES['scrobbles'] = (
    "CREATE TABLE `scrobbles` ("
    "   `discord_id` char(18) NOT NULL,"
    "   `lastfm_username` LONGTEXT NOT NULL,"
    "   `artist` LONGTEXT NOT NULL,"
    "   `track` LONGTEXT NOT NULL,"
    "   `timestamp` int(15) NOT NULL"
    ") ENGINE=InnoDB")
TABLES['usernames'] = (
    "CREATE TABLE `usernames` ("
    "`discord_id` char(18) NOT NULL,"
    "`lastfm_username` LONGTEXT NOT NULL,"
    "PRIMARY KEY(`discord_id`)"
    ") ENGINE=InnoDB")

cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
cursor = cnx.cursor()

for name, ddl in TABLES.items():
    try:
        print("Creating table {}: ".format(name), end='')
        cursor.execute(ddl)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
cnx.close()

"""
Functions for tracking and storing scrobbles.

"""

def add_scrobble_data(scrobble_data):
    cnx = mysql.connector.connect(user='root', database='scrobbles', password='Reverie42!')
    cursor = cnx.cursor()

    add_scrobble = ("INSERT INTO scrobbles "
                  "(discord_id, lastfm_username, artist, track, timestamp) "
                  "VALUES (%(discord_id)s, %(lastfm_username)s, %(artist)s, %(track)s, %(timestamp)s)")
        
    cursor.execute(add_scrobble, scrobble_data)
    cnx.commit()

    cursor.close()
    cnx.close()

"""
Functions for tracking and storing usernames.

"""

def add_username(discord_id, lastfm_username):
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor()

    add_username = ("REPLACE INTO usernames"
                    "(discord_id, lastfm_username) "
                    "VALUES (%(discord_id)s, %(lastfm_username)s)")
    username_data = {
        'discord_id': discord_id,
        'lastfm_username': lastfm_username,
        }
    
    cursor.execute(add_username, username_data)
    cnx.commit()
    
    cursor.close()
    cnx.close()

def get_username(discord_id):
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor(buffered=True)

    get_username = ("SELECT lastfm_username FROM usernames "
                    "WHERE discord_id = '" + discord_id + "'")
    
    cursor.execute(get_username)       
    try:
        lastfm_username = cursor.fetchone()[0]
    except:
        lastfm_username = None

    cursor.close()
    cnx.close()

    return lastfm_username

"""
Functions for finding trending and top artists.

"""

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

def find_top_artists(num_days):
    DB_NAME = 'scrobbles'

    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor()

    time_cap = str(time.time() - 86400 * num_days)

    select_artists = ("SELECT artist FROM scrobbles "
                      "WHERE timestamp < " + time_cap)

    cursor.execute(select_artists)

    top_artist_dict = {}
    for artist in cursor:
        if artist[0] in top_artist_dict:
            top_artist_dict[artist[0]] += 1
        else:
            top_artist_dict[artist[0]] = 1

    cnx.commit()
    cursor.close()
    cnx.close()

    return top_artist_dict


