import psycopg2

DBUSER = "group3"
DBPASS = "group3"

conn = psycopg2.connect(host="dbclass.rhodescs.org", user="group3", password="group3", dbname="group3")
cur = conn.cursor()

def list_foodbanks():
  cur.execute("SELECT * FROM FoodTable")
  rows = cur.fetchall()
  print("Here are the foodbanks:")
  for row in rows:
      print("Food Bank Name:", row[0], "Address:", row[1])

def list_ammen():
  cur.execute("SELECT * FROM Ammenities")
  rows = cur.fetchall()
  print("Here are the ammennities:")
  for row in rows:
      print("Food Bank Name:", row[0], "Description:", row[1])

def list_volunteers():
  cur.execute("SELECT * FROM Volunteer")
  rows = cur.fetchall()
  print("Here are the volunteers:")
  count = 0
  for row in rows:
      print(" ", row[0], ", ", row[1], ", ", row[2], ", ", row[3], ", ", row[4], ", ", row[5], ", ", row[6], ", "  , count)
      count += 1
def list_volunteerhours():
  cur.execute("SELECT * FROM VolunteerSession")
  rows = cur.fetchall()
  print("Here are the volunteers and their hours:")
  count = 0
  for row in rows:
      print(" ", row[0], ", ", row[1], ", ", row[2], ", ", row[3], ", ", row[4] )
    
def add_FoodTable(filename): #DONE
  with open(filename, 'r') as file:
      next(file) # Skip the header row.
      cur.copy_from(file, 'foodtable', sep=',') #file -> foodtable in sql
  conn.commit()

def add_Staff(filename): #DONE
  with open(filename, 'r') as file:
      next(file) # Skip the header row.
      cur.copy_from(file, 'staff', sep=',') 
  conn.commit()


def add_Volunteer(filename): #DONE
  with open(filename, 'r') as file:
      next(file) # Skip the header row.
      cur.copy_from(file, 'volunteer', sep=',') 
  conn.commit()

def add_VolunteerSession(filename): #DONE
  with open(filename, 'r') as file:
      next(file) # Skip the header row.
      cur.copy_from(file, 'volunteersession', sep=',') 
  conn.commit()

def add_VisitorVisited(filename): # DONE
  with open(filename, 'r') as file:
      next(file) # Skip the header row.
      cur.copy_from(file, 'visitorvisited', sep=',') 
  conn.commit()


def add_GeoData(filename):  #DONE
  with open(filename, 'r') as file:
      next(file) # Skip the header row.
      cur.copy_from(file, 'geodata', sep=',') 
  conn.commit()

def add_Amenities(filename): #DONE
  with open(filename, 'r') as file:
      next(file) # Skip the header row.
      cur.copy_from(file, 'amenities', sep=',') 
  conn.commit()

def add_Owner(filename):  #DONE
  with open(filename, 'r') as file:
      next(file) # Skip the header row.
      cur.copy_from(file, 'owner', sep=',') 
  conn.commit()

def add_Visitors(filename): #DONE
  with open(filename, 'r') as file:
      next(file) # Skip the header row.
      cur.copy_from(file, 'visitors', sep=',') 
  conn.commit()

def add_Rating(filename): #DONE
  with open(filename, 'r') as file:
      next(file) # Skip the header row.
      cur.copy_from(file, 'rating', sep=',') 
  conn.commit()

#never called, should stay empty
def add_foodSupplies(filename):
  with open(filename, 'r') as file:
      next(file) # Skip the header row.
      cur.copy_from(file, 'foodsupplies', sep=',') 
  conn.commit()


def main():
  #list_volunteerhours()
  #list_ammen(
  #list_volunteers()
#  add_VisitorVisited("visitorvisited.csv")
  #add_Amenities('amenities.csv')
  #add_VolunteerSession("volunteeringsession.csv")
  #add_GeoData("geodata.csv")
 # list_foodbanks()
#  add_Staff("staff.csv")
  #add_Rating("ratings.csv")
 #add_Volunteer("volunteers.csv")
  add_Owner("owner.csv")
# call main here when other parts are finished
main()