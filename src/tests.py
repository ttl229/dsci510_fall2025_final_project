# import modules here
from config import *
from database import connect_api_key, add_title_to_database, add_content_to_db
from package.count_followers import get_ig_followers
from package.youtube_scraper import load_comments, scrape_comments
from package.wordcloud_generator import create_word_cloud

### Test Setup Functions ###
key_file = f"{KEYS_DIRECTORY}/youtube_key.txt"
connect_api_key(key_file)       # Takes the key file string as argument, returns the key as a string


### DATABASE MAIN FUNCTIONS - TESTING ###
# # Add Title to Database
show_title = input("Enter title: ")
add_title_to_database(show_title)

# Add content to existing title in database
table_name = 'Genres'
column_name = 'genre'
data = input("Add genre: ")
add_content_to_db(table_name, column_name, data)

### DATA COLLECTION FUNCTIONS - TESTING ###
# Gets follower count from Instagram
username = input("Actor's username: ")
get_ig_followers(username)

# Gets comments from YouTube video
api_key = connect_api_key(key_file)
video_id = input("Video ID: ")
load_comments(video_id, api_key, 1000)


### DATA VISUALIZATION FUNCTIONS - TESTING ###
# Generate word cloud from YouTube Comments
api_key = connect_api_key(key_file)
video_id = 'diCMzPGyFNg'
max_comments = 1000
comments = scrape_comments(video_id, api_key, max_comments)
text = " ".join(comments)
wordcloud = create_word_cloud(text)