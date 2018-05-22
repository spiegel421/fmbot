import mysql.connector, time, discord
from mysql.connector import errorcode
from discord.ext import commands

DB_NAME = 'scrobbles'

TABLES = {}
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

def add_username(discord_id, lastfm_username):
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor()

    add_username = ("INSERT INTO usernames"
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
