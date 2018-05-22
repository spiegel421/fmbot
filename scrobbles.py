import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'scrobbles'

TABLES = {}
TABLES['scrobbles'] = (
    "CREATE TABLE `scrobbles` ("
    "   `discord_id` LONGTEXT NOT NULL,"
    "   `lastfm_username` LONGTEXT NOT NULL,"
    "   `artist` LONGTEXT NOT NULL,"
    "   `track` LONGTEXT NOT NULL,"
    "   `timestamp` int(15) NOT NULL"
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

add_scrobble = ("INSERT INTO scrobbles "
              "(discord_id, lastfm_username, artist, track, timestamp) "
              "VALUES (%(discord_id)s, %(lastfm_username)s, %(artist)s, %(track)s, %(timestamp)s)")

def add_scrobble_data(scrobble_data):
    cnx = mysql.connector.connect(user='root', database='scrobbles', password='Reverie42!')
    cursor = cnx.cursor()
    
    cursor.execute(add_scrobble, scrobble_data)
    cnx.commit()

    cursor.close()
    cnx.close()
