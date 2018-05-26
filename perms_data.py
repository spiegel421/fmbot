import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'perms_data'

TABLES = {}
TABLES['disallows'] = (
    "CREATE TABLE `disallows` ("
    "`channel_id` char(18) NOT NULL,"
    "`cog` LONGTEXT NOT NULL"
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

def add_disallow(channel_id, cog):
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor()

    add_disallow = ("REPLACE INTO disallows "
                    "(channel_id, cog) "
                    "VALUES (%(channel_id)s, %(cog)s)")
    disallow_data = {
        'channel_id': channel_id,
        'cog': cog,
        }
    
    cursor.execute(add_disallow, disallow_data)
    cnx.commit()
    
    cursor.close()
    cnx.close()

def remove_disallow(channel_id, cog):
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor()

    remove_disallow = ("DELETE FROM disallows"
                       "WHERE channel_id = '"+channel_id+"' "
                       "AND `cog` = '"+cog+"'")
    
    cursor.execute(remove_disallow)
    cnx.commit()
    
    cursor.close()
    cnx.close()

def get_disallowed(channel_id, cog):
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor(buffered=True)

    get_disallowed = ("SELECT channel_id FROM disallows "
                      "WHERE cog = '"+cog+"'")
    
    cursor.execute(get_disallowed)       
    if channel_id in cursor:
        disallowed = True
    else:
        disallowed = False

    cursor.close()
    cnx.close()

    return True if disallowed is not None else False
