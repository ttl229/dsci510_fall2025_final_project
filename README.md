# dsci510_fall2025_final_project
USC DSCI510
Project Title: VMDB (Vertical Minidrama Database)
Version: 0.1
Last updated: 11-13-2025
Usage: a database for vertical mini-drama titles

DESCRIPTION:
* This database is in beta mode and currently being updated. 
* The purpose of this database is to track vertical minidrama shows for insight analysis.

GETTING STARTED:
* See requirements.txt for full package requirements


SET-UP:
* Under project folder (parallel to src/) create following folders 'keys', 'data', 'db'
* See Additional Project Details below for recommended project directory structure
* Add your API keys to the 'keys' folder with structure 'platform_key.txt' (example: youtube_key.txt)
* Run the code in 'setup.py' to initialize database from template schema


RUNNING THE PROGRAM:
Step 1. 


---- ADDITIONAL PROJECT DETAILS -----

DATA SOURCES


RESULTS


ANALYSIS


DIRECTORY STRUCTURE: 
project file (root):
|__data/
|__db/              ** database schema file located here
|__documents/       ** additional project documentation and files located here
|__keys/            ** example key folder naming convention below
|   |--youtube_key.txt
|    |--tmdb_key.txt
|__src/             ** main.py located here
|   |--config.py
|   |--main.py
|   |--setup.py
|   |__package      ** program modules located here
|__results/
|__tests/           ** tests.py located here
|   |--tests.py



CHALLENGES:
>>> When trying to extract instagram followers using HTML and Beautiful Soup, I discovered that Instagram does not allow scraping follower count. Need to download Selenium.
