import os


# identifies current directory for project file path mapping
current_directory = os.path.dirname(os.path.abspath(__file__))
# current_directory is also where main.py is located

# project root directory configuration
PROJECT_ROOT_DIRECTORY = os.path.abspath(os.path.join(current_directory, ".."))

# project file structure configuration
PACKAGE_DIRECTORY = os.path.join(current_directory, "package")
DATA_DIRECTORY = os.path.join(PROJECT_ROOT_DIRECTORY, "data")
TESTS_DIRECTORY = os.path.join(PROJECT_ROOT_DIRECTORY, "tests")
RESULTS_DIRECTORY = os.path.join(PROJECT_ROOT_DIRECTORY, "results")
KEYS_DIRECTORY = os.path.join(PROJECT_ROOT_DIRECTORY, "keys")

# database configuration
DATABASE_DIRECTORY = os.path.join(PROJECT_ROOT_DIRECTORY, "db")
schema_file = os.path.join(DATABASE_DIRECTORY, "verticals_database.db.sql")

# data sources configuration



# Other Links
# https://www.verticaldramalove.com/vertical-drama-love-fan-survey-2025