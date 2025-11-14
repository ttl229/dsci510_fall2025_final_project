from functions import add_title_to_database
from imdb_scraper import imdb_title_scraper


# Testing function add_title_to_database
# filepath = '../data/verticals_database.db'
# add_title_to_database("Cheer Up, Baby!", filepath, genre_id='YA', release_date='7/3/25', platform_id='DramaBox')



# Testing IMDB Scraper
url = "https://m.imdb.com/name/nm13604121/?ref_=fn_t_1"
imdb_title_scraper(url)