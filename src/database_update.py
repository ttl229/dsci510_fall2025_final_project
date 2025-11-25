import sqlite3
import csv
import re
import pandas as pd


# Create a new database file from existing schema
def create_new_database(db_file, schema_file):
    conn = None
    try:
        with open(schema_file, 'r') as f:
            sql_script = f.read()

        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.executescript(sql_script)

        conn.commit()
        print(f"Database '{db_file}' successfully created from '{schema_file}'")


    except sqlite3.Error as e:
        print(f"Error creating db file: {e}")

    finally:
        conn.close()

    return db_file





# Insert new data into database from a csv file
csv_file = '../data/db_2025_release_schedule.csv'

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

try:
    with open(csv_file, 'r', newline='') as csvfile:
        print(f"Extracting data from {csv_file}")
        csv_reader = csv.reader(csvfile, delimiter=',')
        next(csv_reader)

        sql_query = f"INSERT INTO Titles (title, release_date) VALUES (?, ?);"

        for row in csv_reader:
            # Gets rid of the prefix before the title string
            clean_title = row[0].split(": ", 1)[-1]

            # Ignores empty strings
            if not clean_title:
                continue

            release_date = row[1]
            params = (clean_title, release_date)
            cursor.execute(sql_query, params)

    conn.commit()
    print(f"Database ({db_file}) has been updated with data from source ({csv_file}).")

except Exception as e:
    print(f"Error: {e}")

finally:
    conn.close()


