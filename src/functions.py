import sqlite3



# Function to allow user to add entries to database
def add_title_to_database(show_title: str, db_path: str, **kwargs) -> str:
    # kwargs: release_date, episodes, platform, genre, cast

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check to see if the title already exists in database
        if_exist_query = "SELECT * FROM titles WHERE title = ?"
        cursor.execute(if_exist_query, (show_title,))
        if cursor.fetchone():
            print('Title already exists.')
            return db_path

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
                cursor.execute(insert_query, (values))
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
        return None

    return db_path

# def add_details_to_title():



