import os
from src.package import imdb_scraper as imdb
from src.package.database import connect_api_key
from src.package import youtube_scraper as youtube
from src.package.youtube_scraper import scrape_comments, get_top_word_cloud
import matplotlib

# identifies current directory for accurate filepath access
current_directory = os.path.dirname(os.path.abspath(__file__))

# Testing function add_title_to_database
# filepath = '../data/verticals_database.db'
# add_title_to_database("Cheer Up, Baby!", filepath, genre_id='YA', release_date='7/3/25', platform_id='DramaBox')


# Testing IMDB Scraper
"""
Using function imdb_title_scraper(url: str) to gather previous titles for actor
"""
# print("Testing IMDB Scraper Function")
# url = input("url: ")
# imdb.imdb_title_scraper(url)


# Testing API Key
filename = "youtube_key.txt"  # Replace with your key file name
key_file = os.path.join(current_directory, "..", "keys", filename)
api_key = connect_api_key(key_file)

# Testing YouTube Comment Scraper
# video_id = "diCMzPGyFNg"
# max_comments = 1000
# youtube.load_comments(video_id, api_key, max_comments)

# Testing YouTube Word Cloud Generator
video_id = "g_C8mLNx6pU"
comments = scrape_comments(video_id, api_key, 1000)
text = " ".join(comments)
get_top_word_cloud(video_id, 50)


# Testing Instagram Scraper
# url = "https://www.instagram.com"
# print("Testing Instagram Scraper Function")
# username = input("Username:")
# get_ig_followers(username)


