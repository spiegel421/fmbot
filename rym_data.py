import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'rym_data'

TABLES = {}
TABLES['usernames'] = (
    "CREATE TABLE `usernames` ("
    "`discord_id` char(18) NOT NULL,"
    "`rym_username` LONGTEXT NOT NULL,"
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
Functions for tracking and storing usernames.

"""

def add_username(discord_id, rym_username):
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor()

    add_username = ("REPLACE INTO usernames"
                    "(discord_id, rym_username) "
                    "VALUES (%(discord_id)s, %(rym_username)s)")
    username_data = {
        'discord_id': discord_id,
        'rym_username': rym_username,
        }
    
    cursor.execute(add_username, username_data)
    cnx.commit()
    
    cursor.close()
    cnx.close()

def get_username(discord_id):
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor(buffered=True)

    get_username = ("SELECT rym_username FROM usernames "
                    "WHERE discord_id = '" + discord_id + "'")
    
    cursor.execute(get_username)       
    try:
        rym_username = cursor.fetchone()[0]
    except:
        rym_username = None

    cursor.close()
    cnx.close()

    return rym_username
