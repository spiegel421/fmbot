import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'perms_data'

TABLES = {}
TABLES['fm'] = (
    "CREATE TABLE `fm` ("
    "`channel_id` char(18) NOT NULL,"
    "PRIMARY KEY (channel_id)"
    ") ENGINE=InnoDB")
TABLES['rym'] = (
    "CREATE TABLE `rym` ("
    "`channel_id` char(18) NOT NULL,"
    "PRIMARY KEY (channel_id)"
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

    add_disallow = ("REPLACE INTO "+cog+" "
                    "(channel_id) "
                    "VALUES (%(channel_id)s)")
    disallow_data = {
        'channel_id': channel_id,
        }
    
    cursor.execute(add_disallow, disallow_data)
    cnx.commit()
    
    cursor.close()
    cnx.close()

def remove_disallow(channel_id, cog):
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor()

    remove_disallow = ("DELETE FROM "+cog+" "
                       "WHERE channel_id = '"+channel_id+"'")
    
    cursor.execute(remove_disallow)
    cnx.commit()
    
    cursor.close()
    cnx.close()

def get_disallowed(channel_id, cog):
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor(buffered=True)

    get_disallowed = ("SELECT channel_id FROM "+cog)
    
    cursor.execute(get_disallowed)       
    if (channel_id,) in cursor:
        disallowed = True
    else:
        disallowed = False

    cursor.close()
    cnx.close()

    return disallowed
