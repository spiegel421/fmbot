import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'scrobbles'
NUM_DAYS = 1

cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
cursor = cnx.cursor()

try:
    cnx.database = DB_NAME  
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

time_cap = str(time.time() - 86400 * NUM_DAYS)

select_artists = ("SELECT artist FROM scrobbles "
                  "WHERE timestamp > " + time_cap)

cursor.execute(select_artists)
cnx.commit()

trending_artist_dict = {}
for i in range(cursor.rowcount):
    row = cursor.fetchone()
    if row[0] in trending_artist_dict:
        trending_artist_dict[row[0]] += 1
    else:
        row[0] = 1

cursor.close()
cnx.close()


print(trending_artist_dict)
