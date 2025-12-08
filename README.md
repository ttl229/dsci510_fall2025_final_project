# dsci510_fall2025_final_project
USC DSCI510
Project Title: VMDB (Vertical Minidrama Database)
Version: 0.2
Last updated: 12-07-25
Usage: a database for vertical mini-drama titles

DESCRIPTION:
* This database is in beta mode. 
* The purpose of this database is to track vertical minidrama shows for insight analysis.

GETTING STARTED:
* See requirements.txt for full package requirements


SET-UP:
* Under project folder (parallel to src/) create following folders 'keys', 'data', 'db'
* See Additional Project Details below for recommended project directory structure
* Add your API keys to the 'keys' folder with file name 'platform_key.txt' (example: youtube_key.txt)
* To set up your database, run main.py and follow the prompts 

HOW TO RUN:
Requirements: requirements.txt
From terminal: Run main.py
From Jupyter Notebook: Run 'results.ipynb' for sample pipeline


---- ADDITIONAL PROJECT DETAILS -----

DATA SOURCES
Data Source 1: IMDB.com
Data Source 2: Instagram.com
Data Source 3: YouTube.com

RESULTS
Loaded database with 300 show titles, 100 actors
Manually added attributes such as genres, role types, view counts due to lack of centralized data



ANALYSIS
- Compared effect of follower count of actors on the overall popularity of show
- Generated word clouds to depict user sentiment for various titles
- Generate list of top actors by hit-rate


DIRECTORY STRUCTURE: 
project file (root):
|__data/
|__db/                  ** database schema file located here
|__documents/           ** additional project documentation and files located here
|__keys/                ** example key folder naming convention below
|   |--youtube_key.txt
|__src/                 ** main.py located here
|   |--__init__.py
|   |--config.py
|   |--main.py
|   |--database.py      ** main program functions located here
|   |--results.ipynb    ** run in jupyter notebook for sample pipeline
|   |--tests.py
|   |__package          ** program modules located here
|__results/
|__tests/              


CHALLENGES:
>>> When trying to extract instagram followers using HTML and Beautiful Soup, I discovered that Instagram does not allow scraping follower count. Need to download Selenium.
