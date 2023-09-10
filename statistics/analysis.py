import pandas as pd
from scipy import stats
import numpy as np


class statistics_analysis:
    def __init__(self, db):
        self.db = db
        # db is an object from database_connector
    

    # define a function for first hypothesis test question:
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
    

    def calculate_mean_change(self, days):
        daily_change = self.db[self.db['day_of_week'].isin(days)]['close'] - self.db[self.db['day_of_week'].isin(days)]['open']
        return daily_change.mean()

    def compare_schedules(self, sched1 = ['Thursday', 'Friday', 'Saturday'], sched2 = ['Sunday', 'Monday', 'Tuesday']):
        mean1 = self.calculate_mean_change(sched1)
        mean2 = self.calculate_mean_change(sched2)

        t_stat, p_value = stats.ttest_ind(sched1, sched2)

        if p_value < 0.05:
            return f"There is a significant difference between the two sets of days (p={p_value})."
        else:
            return f"There is no significant difference between the two sets of days (p={p_value})."
       
            # sched1 and sched2 are two working schedules to compare
         

