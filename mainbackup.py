# basic test script to check database connection
#Will's main before I (mei) imported flask

import psycopg2


DBUSER = "group3"
DBPASS = "group3"

conn = psycopg2.connect(host="dbclass.rhodescs.org", user="group3", password="group3", dbname="group3")
cur = conn.cursor()  # make a cursor (allows us to execute queries)

print("Seems ok!")



cur.close()  
conn.close() # close everything