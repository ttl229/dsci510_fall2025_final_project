import os
from src.package import imdb_scraper as imdb
from src.database_update import update_database_with_json
from src.package.count_followers import get_ig_followers
import sqlite3

""" 
Example of how to load actor data into database using the program functions
"""

# Initializing testing variables
actor_name = input("Actor name: ")
db_file = "../db/verticals_database.db"
json_filepath = ""
data_filepath = ""
testnumber = 1

# helper function
def ask_user_to_continue(counter)-> int:
    test = int(counter)
    print(f"Test {counter} Completed. Continue to next test: y/n?")
    answer = input(" ")

    if answer == "n":
        exit()

    else:
        test = counter + 1
        print(f"Continuing to Test {test}...")

    return test


"""
Test 1: Extracting Actor/Actress Data
Sample Input for Testing
URL: https://www.imdb.com/name/nm12059636/?ref_=fn_t_1
Actor name: Alexa Reddy
"""
# Run code below using sample input to test imdb title scraper
url = input("IMDB url: ")
filename = imdb.imdb_title_scraper(url, actor_name)  # Scrape previous titles for an actor on IMDB
json_filepath = f"../data/imdb_titles/{filename}"   # Stores the output file into variable for testing purposes
# Expected output: up to 15 previous titles saved to file under 'data/imdb_titles' folder under project root


testnumber = ask_user_to_continue(testnumber)


"""
Test 2: Adding Actor/Actress Data to Database
Sample Input for Testing
db filepath: ../db/verticals_database.db
json filepath: use json filepath from Test 1
Actor ID: 1
"""
# Check to make sure db_file is not empty
if not db_file:
    db_file = input('db filepath: ')

# Sets up data filepath for next test
prefix = "../data/imdb_titles/"
postfix = "_imdb_titles.json"
data_filepath = prefix + actor_name + postfix
print(f"Updating database with data from {data_filepath}")

update_database_with_json(db_file, data_filepath, actor_name)
# Expected output: 'Titles' and 'Roles' Table updated in the database

testnumber = ask_user_to_continue(testnumber)

"""
Test 3: Adding Instagram Data to Database
Sample Input for Testing
Actor Instgram Handle = "alexareddy"
"""
# Run code below to test scraping Instagram Data and adding to database
username = input("Actor Instagram Handle: ")
followers = get_ig_followers(username)


# Add data to database
print("Would you like to update database with this data?  y/n")
answer = input(" ")

if answer == 'y':
    print(f"Please confirm actor name is correct before proceeding.\n Actor:{actor_name}")
    print(f"Is this correct? y/n")
    answer = input("")
    if answer == "y":
        print("Thank you for confirming. Adding follower count to database...")
    elif answer == 'n':
        actor_name = input("Actor name: ")

    number_followers = followers

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    update_query = f"""UPDATE Actors 
    SET number_followers = ?
    WHERE name = ?;
    """

    cursor.execute(update_query, (number_followers, actor_name))
    print(f"{actor_name} follower count updated to {number_followers} in database.")
    conn.commit()
    conn.close()

else:
    exit()

print("Testing complete. Goodbye.")

