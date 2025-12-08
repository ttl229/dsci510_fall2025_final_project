from config import *
import csv
import collections
import json
import os
import re
import sqlite3

# Define global variables
db_filename = "verticals_database.db"
db_filepath = os.path.join(DATABASE_DIRECTORY, db_filename)
youtube_keyfile = os.path.join(KEYS_DIRECTORY, "youtube_key.txt")
schema_filepath = os.path.join(DATABASE_DIRECTORY, "verticals_database.db.sql")


# Function to import API key securely
def connect_api_key(key_file: str)->str:  # Returns API key as string
    try:
        with open(key_file, "r") as f: # Reads API Key
            key = f.readline().strip()
        print(f"Using key file: {key_file}")
        return key

    except FileNotFoundError as e:
        print(f"Could not find file {key_file}. Please check the filepath and try again.")
        return ""


# Clean text function to remove punctuation for search
def clean_text(text: str)->str:
    pattern = r'[^\w\s]'
    result = re.sub(pattern, '', text)
    cleaned_text = result.lower().strip()
    return cleaned_text


# Clean text for SQL query
def clean_sql_text(column: str)->str:
    expression = f"LOWER({column})"
    for p in ".,!;:-()":
        expression = f"REPLACE({expression}, '{p}', '')"
    return expression


# Create new database from schema
# Takes two argument: db (name of the db file you want to create) and schema (name of existing schema file)
def create_new_database(db: str, schema: str) ->  str:
    conn = None
    try:
        with open(schema, 'r') as f:
            sql_script = f.read()

        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        cursor.executescript(sql_script)

        conn.commit()
        print(f"Database '{db}' successfully created from '{schema}'")

    except sqlite3.Error as e:
        print(f"Error creating db file: {e}")

    finally:
        conn.close()

    return db


# Get database filepath
def get_database() -> str:

    if os.path.exists(db_filepath):
        print(f"Using database file: {db_filepath}")
        return db_filepath

    else:
        # Create new database
        print("Could not locate existing database in project folder.\n Would you like to create new database file from schema? y/n")
        answer = input(" ")
        if answer == "y":
            create_new_database(db_filename, schema_filepath)

        elif answer == "n":
            print("Please connect your database file to continue running program")

    return ""



# Function to allow user to add entries to database
def add_title_to_database(show_title: str, **kwargs) -> str:
    # kwargs: release_date, episodes, platform, genre, cast
    db = db_filepath

    try:
        conn = sqlite3.connect(db_filepath)
        cursor = conn.cursor()

        # Check to see if the title already exists in database
        if_exist_query = "SELECT * FROM titles WHERE title = ?"
        cursor.execute(if_exist_query, (show_title,))
        if cursor.fetchone():
            print('Title already exists.')
            return db

        # If title does not already exist, add title to database
        else:
            add_title_query = "INSERT INTO titles (title) VALUES (?)"
            cursor.execute(add_title_query, (show_title,))
            conn.commit()

            if kwargs:  # Allows user to pass additional titles directly through command line
                columns = ", ".join(list(kwargs.keys()))
                placeholders = ", ".join(["?" for item in kwargs])
                values = list(kwargs.values())
                insert_query = f" INSERT INTO titles ({columns}) VALUES ({placeholders})"
                cursor.execute(insert_query, values)
                conn.commit()

            else:  # Allows user to manually enter additional title attributes
                print("Would you like to add additional details to title?")
                answer = input("y/n:  ")
                if answer == "y":
                    release_date = input("Release date: ")
                    episodes = int(input("Episodes: "))
                    update_details_query = "UPDATE titles SET release_date = ?, episodes = ? WHERE title = ?"
                    cursor.execute(update_details_query, (release_date, episodes, show_title))
                    print(f"Title '{show_title}' successfully added with attributes: {release_date}, {episodes}")
                else:
                    print(f"Title successfully added: {show_title}")
            conn.close()

    except sqlite3.Error as e:
        # Error exception
        print(f"Error connecting to filepath: {e}")
        return ""

    return db


# Insert new data into database from a csv file
def update_database_with_csv(db_filepath):
    filepath = input('csv filepath: ')
    csv_file = filepath.split(": ", 1)[-1]

    conn = sqlite3.connect(db_filepath)
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
        print(f"Database ({db_filepath}) has been updated with data from source ({csv_file}).")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        conn.close()


# Add JSON data to database
def update_database_with_json(db, json_file, actor_name):
    filepath = json_file

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    try:
        # Check to see if actor exists in database
        actor_exist_query = "SELECT id FROM Actors WHERE name = ?"
        cursor.execute(actor_exist_query, (actor_name,))
        row = cursor.fetchone()

        if row:
            # Gets actor id if actor already exists in database
            actor_id = row[0]
        else:
            # Adds actor as new row in database if not already present
            insert_actor_query = "INSERT INTO Actors (name) VALUES (?);"
            cursor.execute(insert_actor_query, (actor_name,))
            actor_id = cursor.lastrowid

        print(f"Adding roles to {actor_name}")

        # Updates actor row with titles in database
        with open(filepath, 'r') as f:
            json_data = json.load(f)

            insert_title_query = f"INSERT INTO Titles (title) VALUES (?) ON CONFLICT (title) DO NOTHING;"
            select_title_query = f"SELECT id FROM Titles WHERE title = ?"
            insert_role_query = f"INSERT INTO Roles (title_id, actor_id, role) VALUES (?, ?, ?) ON CONFLICT (title_id, role) DO NOTHING;"

            for item in json_data:
                title = item.get('title')
                role = item.get('role')
                cursor.execute(insert_title_query, (title,))
                cursor.execute(select_title_query, (title,))
                result = cursor.fetchone()

                if not result:
                    continue

                # Extracts the title primary key from Titles table as a foreign key reference in Roles table
                title_id = result[0]

                cursor.execute(insert_role_query, (title_id, actor_id, role))

        conn.commit()
        print(f"Database file ({db}) successfully updated with data from source ({filepath}).")

    except Exception as e:
        print(f"Error: {e}")
        return

    finally:
        conn.close()


# Add to existing row in database
def add_content_to_db(table_name: str, column_name: str, content):
    insert_value = content

    conn = sqlite3.connect(db_filepath)
    cursor = conn.cursor()

    try:
        if table_name == "Actors" and column_name == "number_followers":
            actor_name = input("Actor name: ")

            # Check to see if actor exists
            cursor.execute("SELECT id FROM Actors WHERE name = ?", (actor_name,))
            row = cursor.fetchone()

            if row:
                # Updates actors follower count if already exists in database
                update_query = """
                UPDATE Actors 
                SET number_followers = ?
                WHERE name = ?;
                """
                cursor.execute(update_query, (content, actor_name))

            else:
                # Adds new actor row and follower count if actor not already present
                sql_query = f"INSERT INTO {table_name} ({column_name}) VALUES (?, ?)"
                cursor.execute(sql_query, (actor_name, insert_value,))

            print(f"Successfully updated '{column_name}' (column) in '{table_name}' (Table)")

            conn.commit()
            return

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        conn.close()


# Search database functions
def search_by_title(title: str):
    cleaned_title = clean_text(title)  # standardize the title input for easier search

    try:
        conn = sqlite3.connect(db_filepath)
        cursor = conn.cursor()

        sql_cleaned_title = clean_sql_text("title")
        # Removes punctuation and makes title values lower case for search match efficiency

        search_query = f"SELECT id FROM Titles WHERE {sql_cleaned_title} = ?"
        cursor.execute(search_query, (cleaned_title,))      # Checks to see if title exists in database
        search_result = cursor.fetchone()

        if not search_result:
            print("Title not found")
            return None

        title_id = search_result[0]

        # Pulls up details for title
        details_query = """
            SELECT 
                Titles.title, Titles.release_date, Titles.episodes,
                Platforms.name as platform,
                json_group_array(json_object('actor', Actors.name, 'role', Roles.role)) AS actors
        
            FROM Titles
            JOIN Platforms ON Platforms.id = Titles.platform_id
            JOIN Roles ON Roles.title_id = Titles.id
            JOIN Actors ON Actors.id = Roles.actor_id
    
            WHERE Titles.id = ?
            GROUP BY Titles.id
            """

        cursor.execute(details_query, (title_id,))
        title_details = cursor.fetchone()

        for col, val in zip([d[0] for d in cursor.description], title_details):
            print(f"{col:15} : {val}")

    except sqlite3.Error as e:
        print(f"Error occurred: {e}")

    finally:
        conn.close()

# Searches the database by talent name
def search_by_talent(actor: str):
    cleaned_actor = clean_text(actor)  # standardize the title input for easier search

    try:
        conn = sqlite3.connect(db_filepath)
        cursor = conn.cursor()

        sql_cleaned_actor = clean_sql_text("name")
        # Removes punctuation and makes title values lower case for search match efficiency

        search_query = f"SELECT * FROM Actors WHERE {sql_cleaned_actor} = ?"
        cursor.execute(search_query, (cleaned_actor,))  # Checks to see if actor exists in database
        search_result = cursor.fetchone()

        if not search_result:
            print("Actor not found")
            return None

        # Prints the results for the user
        actor_name = search_result[1]
        actor_titles = search_result[2]
        actor_followers = search_result[3]
        print(f"  {actor_name}\n  {actor_titles} Titles\n  {actor_followers} Followers")

    except sqlite3.Error as e:
        print(f"Error occurred: {e}")

    finally:
        conn.close()


# Function to count the top words used in comments per video
def count_words(video_id:str, number_of_words: int):
    """
    Returns a dictionary of the top number of words found in comments of a video
    Example usage: Returns dictionary of top 10 most used words in comment section of a video
    """
    datafile = os.path.join(DATA_DIRECTORY, f"youtube_comments/{video_id}_youtube_comments.csv")

    all_words = collections.Counter()
    # List of basic words to ignore in counter
    stop_words = ["the", "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "in", "out", "on", "off", "then", "once", "here", "there", "when", "how", "all", "any", "each", "few", "more", "most", "some", "such", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

    try:
        with open(datafile, "r", encoding="utf-8") as f:
            print(f"Reading all words in comments from video with videoID: {video_id}...")
            reader = csv.reader(f)
            next(reader)  # Skips the header row

            for row in reader:
                comment_text = row[0]       # Extracts the contents from the 'comment_content' column
                # Remove punctuation, special characters from words
                cleaned_text = re.sub(r'[^\w\s]','', comment_text)
                comment_words = cleaned_text.lower().split()

                for word in comment_words:
                    if word in stop_words: # Ignore common connector words
                        continue
                    if word: # Check for empty strings after cleaning
                        all_words[word] += 1

    except FileNotFoundError as e:
        print(f"Could not find comment data file for {video_id}: {e}")
        return collections.Counter() # Return empty counter

    # Sorts the dictionary by top words
    print(f"Sorting results by {number_of_words} most common words...")
    top_words = all_words.most_common(number_of_words)

    return top_words

def save_results_to_file(data):
    """Save the DATA as a file"""
    print("Would you like to save result to file?")
    answer = input("y/n: ")

    if answer == 'y':
        filename = input("Save file as: ")
        filepath = os.path.join(DATA_DIRECTORY, filename)
        data.to_file(filepath)
        print(f"Data saved to file: {filepath}")

    return None

# Return to menu
def main_menu():

    # Print Main Menu Options
    print("~~ Menu ~~\n  1. Add Title  \n  2. Search Titles  \n  3. Analyze Titles  \n  4. Quit\n")
    user_choice = int(input(" "))

    if user_choice == 1:  # Allows user to add title to database
        print("Add Title to database")
        show_title = input("Title: ")
        add_title_to_database(show_title)

    elif user_choice == 2:  # Allows user to search the database
        print("Search by:\n 1. Title \n 2. Cast \n 3. Return to main menu")
        search_choice = input(" ")

        match search_choice:
            case "1" | "Title":
                print("Search by title:")
                title = input("Title: ")
                search_by_title(title)

            case "2" | "Cast":
                print("Search by talent:")
                actor = input("Actor/Actress: ")
                search_by_talent(actor)

            case "3" | "Menu":
                main_menu()

            case _:
                print("Please select one of the options above or type 'Menu' to return to main menu.")

    # if user_choice == 3:  # Allows user to analyze titles in database
    #     print("Select an option:\n 1. ")

    if user_choice == 4:  # Exits program
        print("Okay, goodbye.")
        exit(0)
