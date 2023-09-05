import os
import sqlalchemy
from dotenv import load_dotenv
from MySQLdb import _mysql

load_dotenv()


class DatabaseConnector:
    def __init__(self, db_name, db_user, db_password, db_host, db_port):
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port

    def create_database(self):
        # connect to mysql
        db = _mysql.connect(
            host=self.db_host, user=self.db_user, password=self.db_password
        )

        # create database
        db.query(f"""Create database {self.db_name};""")

    def connect_to_db(self):
        # create engine
        engine = sqlalchemy.create_engine(
            f"mysql+mysqldb://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        )

        # create connection
        connection = engine.connect()

        return engine, connection

