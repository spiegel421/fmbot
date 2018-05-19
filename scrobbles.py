import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'scrobbles'

TABLES = {}
TABLES['scrobbles'] = (
    "CREATE TABLE `scrobbles` ("
    "   `discord_user` varchar(100) NOT NULL,"
    "   `lastfm_username` varchar(100) NOT NULL,"
    "   `artist` varchar(100) NOT NULL,"
    "   `track` varchar(200) NOT NULL,"
    "   `timestamp` int(15) NOT NULL"
    ") ENGINE=InnoDB")

cnx = mysql.connector.connect(user='root', database='scrobbles', password='Reverie42!')
cursor = cnx.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cnx.database = DB_NAME  
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

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
              "(discord_user, lastfm_username, artist, track, timestamp) "
              "VALUES (%(discord_user)s, %(lastfm_username)s, %(artist)s, %(track)s, %(timestamp)s)")

def add_scrobble_data(scrobble_data):
    cnx = mysql.connector.connect(user='root', database='scrobbles', password='Reverie42!')
    cursor = cnx.cursor()
    
    cursor.execute(add_scrobble, scrobble_data)
    cnx.commit()

    cursor.close()
    cnx.close()
