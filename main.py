# Blog Flask application

import psycopg2
import psycopg2.extras
from flask import Flask, g, render_template, request
from psycopg2.sql import NULL

# constants
DBUSER = "group3"
DBPASS = "group3"

# debugging?1
DEBUG = True

# initialize Flask
app = Flask(__name__)

####################################################
# Routes

# browse food banks using volunteers or reviews??
#


## Index, not Home page
@app.route("/")
def index():
  return render_template('home.html')

@app.route("/viewownerinfo")
def ownerViewer():
  conn = get_db()
  cursor = conn.cursor()
  #long and scary SQL query, really just gets stuff we need for page
  cursor.execute(
    'SELECT name, address, ownerfirst, ownerlast, foodtable.owneremail AS prof_email, owner.owneremail AS personal_email, income FROM OWNER, foodtable WHERE owner.foodbank_id=foodtable.foodbank_id ORDER BY name asc'
  )
  rowlist = cursor.fetchall()
 
  return render_template('ownerinfo.html', entries = rowlist)

@app.route("/staffdirectory")
def staffdirectory():
  conn = get_db()
  cursor = conn.cursor()
  cursor.execute(
      'select firstname, lastname, email from Staff order by lastname')
  rowlist = cursor.fetchall()
  return render_template('staffdirectory.html', entries=rowlist)


@app.route("/browse")
def browse():
  conn = get_db()
  cursor = conn.cursor()
  cursor.execute(
      #'select foodbank_ID, name, address from FoodTable order by name')
        'select * from staff order by lastname')
  rowlist = cursor.fetchall()
  return render_template('browse.html', entries=rowlist)


# need be able to have button that says sign up from the home/index page
# on signup page, boxes for the names, email, and phone number, a list of all the foodbanks, they choose which one they want, and a button to submit


@app.route("/volunteerhome")
def volunteerhome():
  return render_template('volunteerhome.html')


@app.route("/volsignup", methods=['get', 'post'])
def volsignup():
  if "step" not in request.form:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'select foodbank_ID, name, address from FoodTable order by name')
    rowlist = cursor.fetchall()
    return render_template('volsignup.html',
                           food_banks=rowlist,
                           step="compose_entry")
  elif request.form["step"] == "add_entry":
      print("adding entry")
      conn = get_db()
      cursor = conn.cursor()
      cursor.execute('select MAX(volunteerid) from Volunteer')
      max = cursor.fetchall()
      print(max)
      maxplus = int(max[0][0]) + 1
      print(maxplus)
      cursor.execute("insert into Volunteer (firstname, lastname, phonenum, address, email, hoursvolunteered, volunteerid) values (%s, %s, %s, %s, %s, %s, %s)", [request.form['first'], request.form['last'], request.form['phone'], request.form['address'], request.form['email'], request.form['hours'], maxplus] )
  print("added volunteer")
  conn.commit()
  return render_template('volsignup.html', step="add_entry")
  

@app.route("/removevol", methods=['get', 'post'])
def removevol():
  #step 1, display all volunteers in order to figure out what to delete
  if "step" not in request.form:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('select * from Volunteer')
    rowlist = cursor.fetchall()
    return render_template('removevol.html',
                           step="display_entries",
                           entries=rowlist)
  elif request.form["step"] == "delete_entry":
    conn = get_db()
    cursor = conn.cursor()

    # get the postID from the form
    postid = int(request.form["postid"])

    # run our DELETE
    cursor.execute("delete from volunteer where volunteerid=%s", [email])
    conn.commit()
    return render_template("removevol.html", step="delete_entry")

@app.route("/hourslogged", methods=['get','post'])
def hourslogged():
  if "step" not in request.form:
    return hourslogged()
  elif request.form["step"] == "email_received":
    conn = get_db()
    cursor = conn.cursor()
    #cursor.execute('select * from VolunteerSession where volunteeremail=%s', [request.form["volunteeremail"]]')
    rowlist = cursor.fetchall()
    return render_template('hourslogged.html', entries=rowlist)
    



@app.route("/volhours", methods=['get', 'post'])
def volhours():
  if "step" not in request.form:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('select name, address from FoodTable order by name')
    rowlist = cursor.fetchall()
    return render_template('volhours.html',
                           food_banks=rowlist,
                           step="compose_entry")
  elif request.form["step"] == "add_entry":
    print("adding hours to the table")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('select volunteerid from Volunteer where email = %s', [request.form['email']])
    # need to fix whatever is going on with this
    max = cursor.fetchall()
    print(max)
    maxplus = int(max[0][0])


    if (maxplus != NULL): 
      cursor.execute("insert into VolunteerSession(volunteeremail, datevolunteered, hours, foodbankaddr, volunteerid) values (%s, %s, %s, %s, %s)", [request.form['email'], request.form['date'], request.form['hours'], request.form['food_bank'], maxplus])
      conn.commit()
      return render_template('volsignup.html', step="add_entry")
    else:
      return render_template('volsignup.html', step="null_entry")


@app.route("/banksearch", methods=['GET', 'POST'])
def bankfilter():
  conn = get_db()
  cursor = conn.cursor()

  # Step 1: Display search function or filter choices
  if "step" not in request.form:
    return render_template("bankfilter.html", step="search_or_filter")

    # Step 2a: Searching
  elif request.form["step"] == "search":
    # Fetching search Query
    search_query = request.form["searchQuery"]
    print(search_query)

    trimmed = ("%" + search_query + "%")
    print(trimmed)

    # Executes SQL code
    cursor.execute("SELECT * FROM FoodTable NATURAL JOIN amenities WHERE name ILIKE %s", (trimmed, ))
    #cursor.execute("SELECT * FROM FoodTable WHERE name ILIKE '%fatz%'")
    searchResult = cursor.fetchall()
    print(searchResult)

    conn.close()

    # Preps to render search results
    return render_template("bankfilter.html",
                           results=searchResult,
                           step="search_results")

  elif request.form["step"] == "filter":
    # Fetch filter query
    filter_query = request.form["choice"]
    if (filter_query == "Address"):
      sql_query = "SELECT name, address AS choice FROM FoodTable"
    elif (filter_query == "Bank Name"):
      sql_query = "SELECT name AS choice FROM FoodTable"
    elif (filter_query == "Date Founded"):
      sql_query = "SELECT name, DateFounded AS choice FROM FoodTable"
    elif (filter_query == "Owner Email"):
      sql_query = "SELECT name, ownerEmail AS choice FROM FoodTable"
    else:
      sql_query = ""

    print(sql_query)

    #Executes SQL code
    cursor.execute(sql_query)

    filterResult = cursor.fetchall()
    print(filterResult)

    conn.close()

    # Preps to render filter results
    return render_template("bankfilter.html",
                           results=filterResult,
                           step="filter_results")


@app.route("/reviewsbrowse", methods=['get', 'post'])
def reviewsbrowse():
  conn = get_db()
  cursor = conn.cursor()
  cursor.execute(
      'select ReviewerEmail, foodbank, numOfStars from Rating order by ReviewerEmail'
  )
  rowlist = cursor.fetchall()
  return render_template('reviewsbrowse.html', entries=rowlist)


@app.route("/review", methods=['get', 'post'])
def review():
  # step 1: display form
  if "step" not in request.form:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(        
      "SELECT DISTINCT f.foodbank_ID, f.address FROM Rating r JOIN FoodTable f ON r.FoodbankID = f.foodbank_ID"
    )
    rowlist = cursor.fetchall()
    return render_template('review.html',
                           food_banks=rowlist,
                           step="compose_entry")

  # step 2: add review to db
  elif request.form["step"] == "add_entry":
    print("adding entry")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('select MAX(reviewID) from Rating')
    max = cursor.fetchall()
    print(max)
    maxplus = int(max[0][0]) + 1
    print(maxplus)
    cursor.execute(
        "insert into Rating (reviewID, FoodbankID, ReviewerEmail, foodbank, numOfStart) values (%d, %d, %s, %s, %s)",
        [    maxplus, request.form['FoodbankID'],  request.form['ReviewerEmail'],  
             request.form['foodbank'], request.form['numOfStars']
        ])
    conn.commit()
    return render_template('review.html', step="add_entry")


# take a look later
@app.route("/editreviews", methods=['get', 'post'])
def editreviews():
  # Step 1, display form to select which entry to edit
  if "step" not in request.form:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT ReviewerEmail, foodbank, numOfStars FROM Rating')
    rowlist = cursor.fetchall()
    return render_template('editreviews.html',
                           step="display_entries",
                           entries=rowlist)

  # Step 2, get postID from form, SELECT this post from the db, and display
  # a form to edit that post.
  elif request.form["step"] == "make_edits":
    conn = get_db()
    cursor = conn.cursor()
    # get the postID from the form
    postid = int(request.form["postid"])
    debug("Using postid=" + str(postid))

    # query the DB to retrieve that post by ID.  We use fetchone()
    # to retrieve the only row (there can be only one!)
    cursor.execute(
        "select ReviewerEmail foodbank, numOfStars from Rating where id=%s",
        [postid])
    row = cursor.fetchone()
    debug("db retrieved: " + str(dict(row)))

    return render_template("editreviews.html", step="make_edits", entry=row)

  # Step 3, user has changed post, now update the DB with changes
  elif request.form["step"] == "update_database":
    conn = get_db()
    cursor = conn.cursor()

    # get the postID from the form
    postid = int(request.form["postid"])

    # run our UPDATE
    cursor.execute(
        "update Rating set ReviewerEmail=%s, foodbank=%s where id=%s",
        [request.form['ReviewerEmail'], request.form['foodbank'], postid])
    conn.commit()
    return render_template("editreviews.html", step="update_database")


# felt that </3
# tbh i was gonna work on this but now i dont feel like it anymore\
# i just wanna rest & not do work :sob:


def connect_db():
  """Connects to the database."""
  debug("Connecting to DB.")
  conn = psycopg2.connect(host="dbclass.rhodescs.org",
                          user=DBUSER,
                          password=DBPASS,
                          dbname="group3",
                          cursor_factory=psycopg2.extras.DictCursor)
  return conn


def get_db():
  """Retrieve the database connection or initialize it. The connection
  is unique for each request and will be reused if this is called again.
  """
  if "db" not in g:
    g.db = connect_db()

  return g.db


@app.teardown_appcontext
def close_db(e=None):
  """If this request connected to the database, close the
  connection.
  """
  db = g.pop("db", None)

  if db is not None:
    db.close()
    debug("Closing DB")


#####################################################
# Debugging


def debug(s):
  """Prints a message to the console/shell (not web browser) 
  if debugging is turned on."""
  if DEBUG:  # set to False to turn off
    print("DEBUG:", s)


#####################################################
# App begins running here:

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080,
          debug=True)  # can turn off debugging with False
