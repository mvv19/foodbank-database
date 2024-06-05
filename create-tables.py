# Script to read the schema.sql file and execute the commands
# inside to create all of our (initially empty) tables.

import psycopg2

DBUSER = "group3"
DBPASS = "group3"

conn = psycopg2.connect(host="dbclass.rhodescs.org", user="group3", password="group3", 
                        dbname="group3")
cur = conn.cursor()  # make a cursor (allows us to execute queries)


file = open("schematargeted.sql", "r") # open the file
alltext = file.read() # read all the text
cur.execute(alltext) # execute all the SQL in the file
conn.commit()  # Actually make the changes to the db

cur.close()  
conn.close() # close everything