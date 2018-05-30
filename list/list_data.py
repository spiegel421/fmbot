import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'list_data'

TABLES = {}
TABLES['lists'] = (
    "CREATE TABLE `lists` ("
    "   `discord_id` char(18) NOT NULL,"
    "   `list_name` LONGTEXT NOT NULL,"
    "   `editors` LONGTEXT NOT NULL"
    ") ENGINE=InnoDB")
TABLES['current_lists'] = (
    "CREATE TABLE `current_lists` ("
    "   `discord_id` char(18) NOT NULL,"
    "   `current_list` LONGTEXT NOT NULL,"
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

def create_list(discord_id, list_name):
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor(buffered=True)
    
    name = discord_id + "_" + list_name
    create = (
        "CREATE TABLE `{}` ("
        "   `index` INT NOT NULL,"
        "   `item` LONGTEXT NOT NULL,"
        "   `link` LONGTEXT"
        ") ENGINE=InnoDB".format(name)
        )
    cursor.execute(create)

    insert = "INSERT INTO `lists` VALUES ('{0}', '{1}', '{0}')".format(discord_id, list_name)
    cursor.execute(insert)

    cnx.commit()
    cursor.close()
    cnx.close()

def delete_list(discord_id, list_name):    
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor()
    
    name = discord_id + "_" + list_name
    drop = "DROP TABLE `{}`".format(name)
    cursor.execute(drop)

    delete = (
        "DELETE FROM `lists` "
        "WHERE `discord_id` = '{}' "
        "AND `list_name` = '{}'".format(discord_id, list_name)
        )
    cursor.execute(delete)

    cnx.commit()
    cursor.close()
    cnx.close()

def get_user_lists(discord_id):
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor()

    select = "SELECT `list_name` FROM `lists` WHERE `discord_id` = '{}'".format(discord_id)
    cursor.execute(select)

    user_lists = []
    for (list_name) in cursor:
        user_lists.append(list_name)

    cursor.close()
    cnx.close()

    return user_lists

def get_list(discord_id, list_name):
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor(buffered=True)

    find = (
        "SELECT * FROM `lists` "
        "WHERE `discord_id` = '{}' "
        "AND `list_name` = '{}'".format(discord_id, list_name)
        )
    cursor.execute(find)
    if cursor.rowcount == 0:
        raise Exception("That is not a list.")

    name = discord_id + "_" + list_name
    select = "SELECT `index`, `item`, `link` FROM `{}`".format(name)
    cursor.execute(select)

    list_dict = {}
    for (index, item, link) in cursor:
        list_dict[index] = (item, link)

    cursor.close()
    cnx.close()

    return list_dict

def get_editors(discord_id, list_name):
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor(buffered=True)

    find = (
        "SELECT `editors` FROM `lists` "
        "WHERE `discord_id` = '{}' "
        "AND `list_name` = '{}'".format(discord_id, list_name)
        )
    cursor.execute(find)
    if cursor.rowcount == 0:
        raise Exception("That is not a list.")

    result = None
    for (editors) in cursor:
        result = editors[0]
    result = result.split(" ")

    cursor.close()
    cnx.close()
    
    return result

def add_editor(discord_id, list_name, editor_id):
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor(buffered=True)

    find = (
        "SELECT `editors` FROM `lists` "
        "WHERE `discord_id` = '{}' "
        "AND `list_name` = '{}'".format(discord_id, list_name)
        )
    cursor.execute(find)
    if cursor.rowcount == 0:
        raise Exception("That is not a list.")

    result = None
    for (editors) in cursor:
        result = editors[0]

    update = (
        "UPDATE `lists` "
        "SET `editors` = '{}' "
        "WHERE `discord_id` = '{}' "
        "AND `list_name` = '{}'".format(result+" "+editor_id, discord_id, list_name)
        )
    cursor.execute(update)

    cnx.commit()
    cursor.close()
    cnx.close()

def add_to_list(list_name, index, item, link):
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor(buffered=True)
    
    select = "SELECT * FROM `{}`".format(list_name)
    cursor.execute(select)
    added_to_end = (index == -1)
    index = cursor.rowcount if (index > cursor.rowcount or index < 0) else index

    if not added_to_end:
        update = (
            "UPDATE `{}` SET `index` = {} "
            "WHERE `index` >= {}".format(list_name, "`index` + 1", index)
            )
        cursor.execute(update)
        
    insert = "INSERT INTO `{}` VALUE('{}', '{}', '{}')".format(list_name, index, item, link)
    cursor.execute(insert)

    cnx.commit()
    cursor.close()
    cnx.close()

def remove_from_list(list_name, index):
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor(buffered=True)
    
    select = "SELECT * FROM `{}`".format(list_name)
    cursor.execute(select)
    removed_from_end = (index == cursor.rowcount - 1)
    index = cursor.rowcount - 1 if (index > cursor.rowcount or index < 0) else index
    
    insert = "DELETE FROM `{}` WHERE `index` = {}".format(list_name, index)
    cursor.execute(insert)

    if not removed_from_end:
        update = (
            "UPDATE `{}` SET `index` = {} "
            "WHERE `index` > {}".format(list_name, "`index` - 1", index)
            )
        cursor.execute(update)
    
    cnx.commit()
    cursor.close()
    cnx.close()

def get_current_list(discord_id):
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor()

    select = "SELECT `current_list` FROM `current_lists` WHERE `discord_id` = '{}'".format(discord_id)
    cursor.execute(select)

    result = None
    for (current_list) in cursor:
        result = current_list[0]

    cursor.close()
    cnx.close()
    
    return result

def switch_current_list(discord_id, list_name, editor_id):
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor()

    name = discord_id + "_" + list_name
    replace = "REPLACE INTO `current_lists` VALUE ('{}', '{}')".format(editor_id, name)
    cursor.execute(replace)

    cnx.commit()
    cursor.close()
    cnx.close()
