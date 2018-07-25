import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'chart_data'

TABLES = {}
TABLES['charts'] = (
    "CREATE TABLE `charts` ("
    "   `discord_id` char(18) NOT NULL,"
    "   `chart_name` LONGTEXT NOT NULL,"
    "   `chart_text` LONGTEXT NOT NULL"
    ") ENGINE=InnoDB")
TABLES['current_charts'] = (
    "CREATE TABLE `current_charts` ("
    "   `discord_id` char(18) NOT NULL,"
    "   `current_chart` LONGTEXT NOT NULL,"
    "   PRIMARY KEY(`discord_id`)"
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

def create_chart(discord_id, chart_name, chart_text):
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor(buffered=True)
    
    name = discord_id + "_" + chart_name

    insert = "INSERT INTO `charts` VALUES ('{0}', '{1}', '{2}')".format(discord_id, chart_name, chart_text)
    cursor.execute(insert)

    cnx.commit()
    cursor.close()
    cnx.close()

def delete_chart(discord_id, chart_name):    
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor()
    
    name = discord_id + "_" + chart_name
    drop = "DROP TABLE `{}`".format(name)
    cursor.execute(drop)

    delete = (
        "DELETE FROM `charts` "
        "WHERE `discord_id` = '{}' "
        "AND `chart_name` = '{}'".format(discord_id, chart_name)
        )
    cursor.execute(delete)

    cnx.commit()
    cursor.close()
    cnx.close()

def get_user_charts(discord_id):
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor()

    select = "SELECT `chart_name` FROM `charts` WHERE `discord_id` = '{}'".format(discord_id)
    cursor.execute(select)

    user_charts = []
    for (chart_name) in cursor:
        user_charts.append(chart_name)

    cursor.close()
    cnx.close()

    return user_charts

def get_chart(discord_id, chart_name):
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor(buffered=True)

    find = (
        "SELECT * FROM `charts` "
        "WHERE `discord_id` = '{}' "
        "AND `chart_name` = '{}'".format(discord_id, chart_name)
        )
    cursor.execute(find)
    if cursor.rowcount == 0:
        raise Exception("That is not a chart.")

    name = discord_id + "_" + chart_name
    select = "SELECT `index`, `item`, `link` FROM `{}`".format(name)
    cursor.execute(select)

    chart_dict = {}
    for (index, item, link) in cursor:
        chart_dict[index] = (item, link)

    cursor.close()
    cnx.close()

    return chart_dict

def add_to_chart(chart_name, index, item, link):
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor(buffered=True)
    
    select = "SELECT * FROM `{}`".format(chart_name)
    cursor.execute(select)
    added_to_end = (index == -1)
    index = cursor.rowcount if (index > cursor.rowcount or index < 0) else index

    if not added_to_end:
        update = (
            "UPDATE `{}` SET `index` = {} "
            "WHERE `index` >= {}".format(chart_name, "`index` + 1", index)
            )
        cursor.execute(update)
        
    insert = "INSERT INTO `{}` VALUE('{}', '{}', '{}')".format(chart_name, index, item, link)
    cursor.execute(insert)

    cnx.commit()
    cursor.close()
    cnx.close()

def remove_from_chart(chart_name, index):
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor(buffered=True)
    
    select = "SELECT * FROM `{}`".format(chart_name)
    cursor.execute(select)
    removed_from_end = (index == cursor.rowcount - 1)
    index = cursor.rowcount - 1 if (index > cursor.rowcount or index < 0) else index
    
    insert = "DELETE FROM `{}` WHERE `index` = {}".format(chart_name, index)
    cursor.execute(insert)

    if not removed_from_end:
        update = (
            "UPDATE `{}` SET `index` = {} "
            "WHERE `index` > {}".format(chart_name, "`index` - 1", index)
            )
        cursor.execute(update)
    
    cnx.commit()
    cursor.close()
    cnx.close()

def get_current_chart(discord_id):
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor()

    select = "SELECT `current_chart` FROM `current_charts` WHERE `discord_id` = '{}'".format(discord_id)
    cursor.execute(select)

    result = None
    for (current_chart) in cursor:
        result = current_chart[0]

    cursor.close()
    cnx.close()
    
    return result

def switch_current_chart(discord_id, chart_name, editor_id):
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor()

    name = discord_id + "_" + chart_name
    replace = "REPLACE INTO `current_charts` VALUE ('{}', '{}')".format(editor_id, name)
    cursor.execute(replace)

    cnx.commit()
    cursor.close()
    cnx.close()
