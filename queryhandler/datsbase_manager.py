from models import Coin, CoinTag, CoinHistory, Tag
import os
import pandas as pd
import json
import datetime
from sqlalchemy.sql import select


class DatabaseManager:
    def __init__(self, db_connector):
        self.db_connector = db_connector
        self.engine, self.connection = self.db_connector.connect_to_db()

    def insert_coin_tag_data(self, coin_tag_data_path):
        with open(coin_tag_data_path, "r") as json_file:
            data = json.load(json_file)

        # Create a connection
        connection = self.engine.connect()

        try:
            # Iterate through the JSON data and insert tags and relationships
            for url, tag_data in data.items():
                # Extract the coin ID from the URL (e.g., "bitcoin" from "/currencies/bitcoin/")
                coin_name = url.split("/")[-2]

                # Query the database to find the correct coin_id based on coin_name
                coin = connection.execute(
                    select(Coin).filter_by(name=coin_name)
                ).fetchone()

                if coin:
                    # Iterate through tags for this coin
                    for tag_title in tag_data.get(f"{coin.name}_Tags", []):
                        # Insert the tag if it doesn't exist
                        tag = connection.execute(
                            select(Tag).filter_by(title=tag_title)
                        ).fetchone()
                        if not tag:
                            connection.execute(
                                Tag.__table__.insert().values(title=tag_title)
                            )
                            connection.commit()

                        # Check if the relationship already exists
                        # we fetch tag again to ensure having access to it's id
                        tag = connection.execute(
                            select(Tag).filter_by(title=tag_title)
                        ).fetchone()
                        existing_relationship = connection.execute(
                            select(CoinTag).filter_by(coin=coin.id, tag=tag.id)
                        ).fetchone()
                        if not existing_relationship:
                            # Insert the relationship between coin and tag
                            connection.execute(
                                CoinTag.__table__.insert().values(
                                    coin=coin.id, tag=tag.id
                                )
                            )
            # Commit the changes
            connection.commit()
        finally:
            # Close the connection in a 'finally' block to ensure it's always closed
            connection.close()

    def insert_coin_data(self, coin_data_path):
        df = pd.read_csv(coin_data_path)
        with self.engine.connect() as connection:
            # Insert data into the coins table
            for index, row in df.iterrows():
                coin = Coin(
                    name=row["Name"],
                    symbol=row["Symbol"],
                    main_link=row["Main Link"],
                    history_link=row["Historical Link"],
                )

                # You can also set other columns here if needed
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
            connection.close()  # think we can omit this line

    @staticmethod
    def get_proper_datetime_format(date):
        """
        To insert a datetime value in mysql, it must have a specific format.
        This function, returns the proper datetime format.
        """
        datetime_obj = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
        return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")

    def get_coin_by_name(self, coin_name):
        query = select(Coin).where(Coin.name == coin_name)
        return self.connection.execute(query).fetchone()

    def insert_coin_history_data(self):
        coin_history_path = os.environ.get("ALL_365_DAYS_PATH")
        # iterate through coin history csv files
        for file in os.listdir(coin_history_path):
            # read csv file
            try:
                df = pd.read_csv(os.path.join(coin_history_path, file), delimiter=";")
            except pd.errors.EmptyDataError:  # handle empty csv files
                print(file)

            # get coin using csv filename
            coin = self.get_coin_by_name(file.split("_")[0])
            # iterate over df rows
            for index, row in df.iterrows():
                self.connection.execute(
                    CoinHistory.__table__.insert().values(
                        coin=coin.id,
                        timestamp=self.get_proper_datetime_format(row["timestamp"]),
                        market_cap=row["marketCap"],
                        open=row["open"],
                        rank=None,  # TODO: need a way to get rank for each coin
                        low=row["low"],
                        high=row["high"],
                        close=row["close"],
                        volume=row["volume"],
                        time_open=self.get_proper_datetime_format(row["timeOpen"]),
                        time_close=self.get_proper_datetime_format(row["timeClose"]),
                        time_high=self.get_proper_datetime_format(row["timeHigh"]),
                        time_low=self.get_proper_datetime_format(row["timeLow"]),
                    )
                )

                # Commit the transaction
                self.connection.commit()
