import os
from database_connector import DatabaseConnector
from datsbase_manager import DatabaseManager

# create a DatabaseConnector object
db_connector = DatabaseConnector(
    db_name=os.environ.get("DATABASE_NAME"),
    db_user=os.environ.get("DATABASE_USER"),
    db_password=os.environ.get("DATABASE_PASSWORD"),
    db_host=os.environ.get("DATABASE_HOST"),
    db_port=os.environ.get("DATABASE_PORT"),
)

# create database
db_connector.create_database()

# create tables
db_connector.create_tables()

# Create a DatabaseManager instance
db_manager = DatabaseManager(db_connector)

# Define the path to the JSON file
coin_tag_data_path = os.environ.get("COIN_TAG_DATA_PATH")
coin_data_path = os.environ.get("COIN_DATA_PATH")

# Call the function to insert data
db_manager.insert_coin_data(coin_data_path)
db_manager.insert_coin_tag_data(coin_tag_data_path)

db_manager.insert_coin_history_data()
