import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'scrobbles'

cnx = mysql.connector.connect(user='root', host='localhost', database=DB_NAME, password='Reveri42!')
cursor = cnx.cursor()
cursor.close()
cnx.close()

def trending_artists(num_days):
    time_cap = str(time.time() - 86400 * num_days)

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


print(trending_artists(1))
