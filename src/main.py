from src.package import database as db
from src.package import youtube_scraper as youtube
import sys

def main():
    print("Library of Vertical Dramas (beta v.0)")
    filepath = '../data/verticals_database.db'

    # Menu
    print("~~ Menu ~~\n  1. Add Title  \n  2. Search Titles  \n  3. Analyze Titles  \n  4. Quit\n")
    user_choice = int(input(" "))
    if user_choice == 1:  # Allows user to add title to database
        print("Add Title to database")
        show_title = input("Title: ")
        db.add_title_to_database(show_title, filepath)

    # if user_choice == 2:  # Allows user to search the database
    #
    # if user_choice == 3:  # Allows user to analyze titles in database
    #     print("")

    if user_choice == 4:  # Exits program
        print("Okay, goodbye.")
        sys.exit


if __name__ == '__main__':
    main()




