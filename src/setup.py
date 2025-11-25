from database_update import create_new_database

""" 
Run this code to set up your initial database using the template schema
"""


db_file = '../db/verticals_database.db'
schema_file = '../db/verticals_database.db.sql'
print(f"Creating new database from {schema_file}")
create_new_database(db_file, schema_file)
print("Process complete.")