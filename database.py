
import sqlite3 as lite
import pandas as pd
import sys as sys

try:
    month = (sys.argv[1])
except IndexError:
    month = ('July')

if month not in ['January','February','March','April','May','June','July','August','September','October','November','December']:
    month = raw_input("Please enter a month as a string: ")

# Connect to the database
con = lite.connect('getting_started.db')

cities = (
    ('New York City', 'NY'),
    ('Boston', 'MA'),
    ('Chicago', 'IL'),
    ('Miami', 'FL'),
    ('Dallas', 'TX'),
    ('Seattle', 'WA'),
    ('Portland', 'OR'),
    ('San Francisco', 'CA'),
    ('Los Angeles', 'CA')
)

weather = (
    ('New York City', 2013, 'July', 'January', 62),
    ('Boston', 2013, 'July', 'January', 59),
    ('Chicago', 2013, 'July', 'January', 59),
    ('Miami', 2013, 'August', 'January', 59),
    ('Dallas', 2013, 'July', 'January', 59),
    ('Seattle', 2013, 'July', 'January', 59),
    ('Portland', 2013, 'July', 'December', 59),
    ('San Francisco', 2013, 'September', 'December', 59),
    ('Los Angeles', 2013, 'September', 'December', 59)
)

with con:
    cur = con.cursor()
    # Create the cities and weather tables
    cur.execute("DROP TABLE IF EXISTS cities")
    cur.execute("DROP TABLE IF EXISTS weather")
    cur.execute("CREATE TABLE cities (name text, state text)")
    cur.execute(
        "CREATE TABLE weather (city text, year integer, warm_month text, cold_month text, average_high integer)")

    # Insert data into the two tables
    cur.executemany("INSERT INTO cities VALUES(?,?)", cities)
    cur.executemany("INSERT INTO weather VALUES(?,?,?,?,?)", weather)

    # Join the data together
    cur.execute("""SELECT name, state FROM cities
        INNER JOIN weather ON name = city
        where warm_month = '{}'""".format(month))

    # Load into a pandas DataFrame
    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    df = pd.DataFrame(rows, columns=cols)

    # Print out the resulting city and state in a full sentence.
    # For example: "The cities that are warmest in July are: Las Vegas, NV, Atlanta, GA..."
    warm_cities = []
    for i in range(df.shape[0]):
        warm_cities.append([df.get_value(i, 'name'), df.get_value(i, 'state')])
    if len(warm_cities) == 0:
        print("No cities have the warmest month in {}".format(month))
    else:
        print("The cities that are warmest in {} are: ".format(month))
        for city in warm_cities:
            print("\t{}, {}".format(city[0],city[1]))
