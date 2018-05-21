import mysql.connector
import time, discord
from mysql.connector import errorcode

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
    
def load_usernames():
    client = discord.Client()
    
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor()

    add_username = ("INSERT INTO usernames"
                    "(discord_id, lastfm_username) "
                    "VALUES (%(discord_id)s, %(lastfm_username)s)")

    reader = open("usernames.txt", 'r')
    for line in reader.readlines():
        lastfm_username = line[1]
        try:
            discord_id = client.users.get('name', line[0]).id
        except:
            continue
        username_data = {
            'discord_id': discord_id,
            'lastfm_username': lastfm_username,
            }
        cursor.execute(add_username, username_data)
        cnx.commit()

    cursor.close()
    cnx.close()

load_usernames()
