import os
from database_connector import DatabaseConnector


# create a DatabaseConnector object
db_connector = DatabaseConnector(
    db_name=os.environ.get("DATABASE_NAME"),
    db_user=os.environ.get("DATABASE_USER"),
    db_password=os.environ.get("DATABASE_PASSWORD"),
    db_host=os.environ.get("DATABASE_HOST"),
    db_port=os.environ.get("DATABASE_PORT"),
)

db_connector.create_tables()
