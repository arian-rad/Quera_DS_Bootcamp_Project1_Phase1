from models import (
    Coin,
    CoinTag,
    Tag
)
import os
import pandas as pd
import json
from database_connector import DatabaseConnector

from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select

class DatabaseManager:
    def __init__(self, db_connector):
        self.db_connector = db_connector
        self.engine, _ = self.db_connector.connect_to_db()

    def insert_coin_tag_data(self, coin_tag_data_path):
            with open(coin_tag_data_path, 'r') as json_file:
                data = json.load(json_file)

            # Create a connection
            connection = self.engine.connect()
            
            try:
                # Iterate through the JSON data and insert tags and relationships
                for url, tag_data in data.items():
                    # Extract the coin ID from the URL (e.g., "bitcoin" from "/currencies/bitcoin/")
                    coin_name = url.split('/')[-2]

                    # Query the database to find the correct coin_id based on coin_name
                    coin = connection.execute(select(Coin).filter_by(name=coin_name)).fetchone()

                    if coin:
                        # Iterate through tags for this coin
                        for tag_title in tag_data.get(f"{coin.name}_Tags", []):
                            # Insert the tag if it doesn't exist
                            tag = connection.execute(select(Tag).filter_by(title=tag_title)).fetchone()
                            if not tag:
                                connection.execute(Tag.__table__.insert().values(title=tag_title))
                                connection.commit()

                            # Check if the relationship already exists \ we fetch tag again to ensure haveing access to it's id
                            tag = connection.execute(select(Tag).filter_by(title=tag_title)).fetchone()
                            existing_relationship = connection.execute(
                                select(CoinTag).filter_by(coin=coin.id, tag=tag.id)
                            ).fetchone()
                            if not existing_relationship:
                                # Insert the relationship between coin and tag
                                connection.execute(CoinTag.__table__.insert().values(coin=coin.id, tag=tag.id))
                # Commit the changes
                connection.commit()
            finally:
                # Close the connection in a finally block to ensure it's always closed
                connection.close()

    def insert_coin_data(self, coin_data_path):
        df = pd.read_csv(coin_data_path)
        with self.engine.connect() as connection:
            # Insert data into the coins table
            for index, row in df.iterrows():
                coin = Coin(name=row['Name'],
                            symbol=row['Symbol'],
                            main_link=row['Main Link'],
                            history_link=row['Historical Link'])
                
                # You can also set other columns herse if needed
                coin.logo = None  # Set to None or a file path/URL if you have logo data
                coin.official_links = None  # Set to appropriate JSON data
                coin.socials = None  # Set to appropriate JSON data
                coin.circulating_supply = None  # Set to the appropriate value

                # Use the connection to insert the coin data
                connection.execute(
                    Coin.__table__.insert().values(
                        name=coin.name,
                        symbol=coin.symbol,
                        logo=coin.logo,
                        official_links=coin.official_links,
                        main_link=coin.main_link,
                        history_link=coin.history_link,
                        socials=coin.socials,
                        circulating_supply=coin.circulating_supply,
                    )
                )
                # Commit the transaction
                connection.commit()
            connection.close()

