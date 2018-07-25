import mysql.connector

DB_NAME = 'fm_data'

cnx = mysql.connector.connect(user='root', database=DB_NAME, password='Reverie42!')
cursor = cnx.cursor()

select = "SELECT * FROM `usernames`"

writer = open("usernames.txt", "w")

cursor.execute(select)
for item in cursor:
    writer.write(cursor)
