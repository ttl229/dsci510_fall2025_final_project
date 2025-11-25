import sqlite3
import csv
import json
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
def update_database_with_csv(db_file):
    filepath = input('csv filepath: ')
    csv_file = filepath.split(": ", 1)[-1]

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        with open(csv_file, 'r', newline='') as csvfile:
            print(f"Extracting data from {csv_file}")
            csv_reader = csv.reader(csvfile, delimiter=',')
            next(csv_reader) # Ignores header row

            sql_query = f"INSERT INTO Actors (name) VALUES (?);"

            for row in csv_reader:
                # Gets rid of the prefix before the title string
                # clean_title = row[0].split(": ", 1)[-1]

                # Ignores empty strings
                # if not clean_title:
                #     continue

                # release_date = row[1]
                # params = (clean_title, release_date)
                name = row[0]
                cursor.execute(sql_query, (name,))

        conn.commit()
        print(f"Database ({db_file}) has been updated with data from source ({csv_file}).")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        conn.close()



# Add JSON data to database
def update_database_with_json(db_file, json_file, actor_name):
    # filepath = input('json filepath: ')
    filepath = json_file
    actor_id = int(input('Actor ID: '))

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        with open(filepath, 'r') as f:
            json_data = json.load(f)

            insert_actorid_query = f"INSERT INTO Actors (id, name) VALUES (?, ?) ON CONFLICT (id) DO NOTHING;"
            insert_title_query = f"INSERT INTO Titles (title) VALUES (?) ON CONFLICT (title) DO NOTHING;"
            select_title_query = f"SELECT id FROM Titles WHERE title = ?"
            insert_role_query = f"INSERT INTO Roles (title_id, actor_id, role) VALUES (?, ?, ?) ON CONFLICT (title_id, role) DO NOTHING;"


            for item in json_data:
                cursor.execute(insert_actorid_query, (actor_id, actor_name))

                title = item.get('title')
                role = item.get('role')

                cursor.execute(insert_title_query, (title,))

                cursor.execute(select_title_query, (title,))

                result = cursor.fetchone()
                if not result:
                    continue
                title_id = result[0]
                # Extracts the title primary key from Titles table as a foreign key reference in Roles table

                cursor.execute(insert_role_query, (title_id, actor_id, role))

        conn.commit()
        print(f"Database file ({db_file}) successfully updated with data from source ({filepath}).")

    except Exception as e:
        print(f"Error: {e}")
        return

    finally:
        conn.close()






