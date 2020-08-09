import sqlite3
import csv
import sys


def main():

    # checking argv (needs to be one, house name)
    if (len(sys.argv) != 2):
        sys.exit("Usage: roster.py house_name")

    # Make house name lower to avoid cap sensitivity
    housename = sys.argv[1].lower()

    # Check if argument is indeed a house at Hogwarts
    houses = ["slytherin", "gryffindor", "ravenclaw", "hufflepuff"]

    if housename.lower() not in houses:
        sys.exit("provide house name: Gryffindor, Hufflepuff, Slytherin or Ravenclaw.")

    # Connect with the .db file and make a cursor
    sqlite_file = "students.db"
    con = sqlite3.connect(sqlite_file)

    cur = con.cursor()

    cur.execute('SELECT first, middle, last, birth FROM students WHERE lower(house) = "{}" ORDER BY last, first;'.format(housename))

    # Fetchall gives us all the rows of the table as a list of tuples with strings.
    houseroster = cur.fetchall()

    # Do stuff with each row in table
    for row in houseroster:

        if not row[1]:
            print("{} {}, born {}".format(row[0], row[2], row[3]))
        else:
            print("{} {} {}, born {}".format(row[0], row[1], row[2], row[3]))

    con.close()


if __name__ == "__main__":
    main()