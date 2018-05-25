import mysql.connector
from mysql.connector import errorcode
from datetime import datetime, timedelta

DB_NAME = 'awol_data'

TABLES = {}
TABLES['timestamps'] = (
    "CREATE TABLE `timestamps` ("
    "`discord_id` char(18) NOT NULL,"
    "`timestamp` DATETIME NOT NULL,"
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

def add_timestamp(discord_id, timestamp):
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor()

    add_timestamp = ("REPLACE INTO usernames"
                    "(discord_id, timestamp) "
                    "VALUES (%(discord_id)s, %(timestamp)s)")
    timestamp_data = {
        'discord_id': discord_id,
        'timestamp': timestamp,
        }
    
    cursor.execute(add_timestamp, timestamp_data)
    cnx.commit()
    
    cursor.close()
    cnx.close()

def get_awol_users():
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor(buffered=True)

    time = datetime.now() - timedelta(seconds=30)
    get_awol_users = ("SELECT discord_id FROM timestamps "
                    "WHERE timestamp < '" + time + "'")
    
    cursor.execute(get_awol_users)
    awol_users = []
    for (discord_id) in cursor:
        awol_users.append(discord_id)

    cursor.close()
    cnx.close()

    return awol_users
