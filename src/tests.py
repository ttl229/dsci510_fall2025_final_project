# import modules here
from src.config import current_directory, KEYS_DIRECTORY
from src.database import connect_api_key


### Test Setup Functions ###
key_file = f"{KEYS_DIRECTORY}/youtube_key.txt"
connect_api_key(key_file)       # Takes the key file string as argument, returns the key as a string



### DATABASE MAIN FUNCTIONS - TESTING ###
# Add Title to Database #



### DATA COLLECTION FUNCTIONS - TESTING ###




### DATA VISUALIZATION FUNCTIONS - TESTING ###