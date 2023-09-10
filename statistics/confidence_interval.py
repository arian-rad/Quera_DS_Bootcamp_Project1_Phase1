import pandas as pd
from scipy import stats
import numpy as np


class statistics_analysis:
    def __init__(self, db):
        self.db = db
        # db is an object from database_connector
    
    def get_confidence_interval(self, n_samples=40):
        # Select the coin names and ids from the coin table
        coins = self.db.query("SELECT id, name FROM coin")

        # Select random n_samples of crypto data
        sample_coins = coins.sample(n=n_samples)

        # Create an empty list to store the mean volume(24h) for every sample
        mean_volumes = []

        # Calculate every sample's mean and append to the list
        for index, row in sample_coins.iterrows():
            volumes = self.db.query(f"SELECT volume FROM coin_history WHERE coin='{row['id']}'")
            mean_volume = volumes['volume'].mean()
            mean_volumes.append(mean_volume)

        # Calculate the 98% confidence interval for the mean volume(24h)
        confidence_interval = stats.norm.interval(0.98, loc=np.mean(mean_volumes), scale=stats.sem(mean_volumes))

        return confidence_interval

