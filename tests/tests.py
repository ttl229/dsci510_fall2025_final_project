from src.package.database import connect_api_key
# from src.package import youtube_scraper as youtube
import os
from src.package.youtube_scraper import scrape_comments, get_top_word_cloud

# identifies current directory for accurate filepath access
current_directory = os.path.dirname(os.path.abspath(__file__))


# Testing function add_title_to_database
# filepath = '../data/verticals_database.db'
# add_title_to_database("Cheer Up, Baby!", filepath, genre_id='YA', release_date='7/3/25', platform_id='DramaBox')


# # Testing IMDB Scraper
# url = "https://m.imdb.com/name/nm13604121/?ref_=fn_t_1"
# db.imdb_title_scraper(url)


# Testing API Key
filename = "youtube_key.txt"  # Replace with your key file name
key_file = os.path.join(current_directory, "..", "keys", filename)
api_key = connect_api_key(key_file)

# Testing YouTube Comment Scraper
video_id = "0SKOObeuGuA"
max_comments = 200
# youtube.load_comments(video_id, api_key, max_comments)

# Testing YouTube Word Cloud Generator
comments = scrape_comments(video_id, api_key, max_comments)
text = " ".join(comments)
get_top_word_cloud(text, 20)
