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

bot = discord.Client(command_prefix='$')

@bot.command()
async def load_usernames():
    cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
    cursor = cnx.cursor()

    add_username = ("INSERT INTO usernames"
                    "(discord_id, lastfm_username) "
                    "VALUES (%(discord_id)s, %(lastfm_username)s)")

    reader = open("usernames.txt", 'r')
    for line in reader.readlines():
        lastfm_username = line.split(',')[1][:-1]
#        try:
        discord_id = bot.users.get('name', line.split(',')[0]).id
 #       except:
#            continue
        username_data = {
            'discord_id': discord_id,
            'lastfm_username': lastfm_username,
            }
        cursor.execute(add_username, username_data)
        
    cnx.commit()
    cursor.close()
    cnx.close()

bot.run('NDQ1ODQzODMwODYwOTM5MjY1.DdzE-g.kffUonxFS9M-0OMCUcwnAYErGYQ')
