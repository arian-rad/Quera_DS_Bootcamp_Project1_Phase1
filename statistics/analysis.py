import pandas as pd
from scipy import stats
import numpy as np


class statistics_analysis:
    def __init__(self, db):
        self.db = db
    # db is an object from database_connector
    

    #### Estimation question:
    
    # define a function to answer the estimation question:
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

        # Calculate and return the 98% confidence interval for the mean volume(24h)
        confidence_interval = stats.norm.interval(0.98, loc=np.mean(mean_volumes), scale=stats.sem(mean_volumes))

        return confidence_interval
    #### in our case The 98% confidence interval for the mean volume(24h) is:
    #### (-105270195.58586341, 474766267.31582564).


    # First hypothesis test question:
    # The null hypothesis in this part states that there is no significant difference between two sets changes mean
    # mathematically: H0: μ1 = μ2
    
    # To answer the first part of the hypothesis test question:
    # First define a function to calculate the mean change in price for each day
    # compare_schedule function calculates the changes mean for each set of days
    # At the end perform t-test to compare two sets
    # sched1 and sched2 are two working schedules to compare
    def calculate_mean_change(self, days):
        daily_change = self.db[self.db['day_of_week'].isin(days)]['close'] - self.db[self.db['day_of_week'].isin(days)]['open']
        return daily_change.mean()
    # sched1 and sched2 are two working schedules to compare
    def compare_schedules(self, sched1 = ['Thursday', 'Friday', 'Saturday'], sched2 = ['Sunday', 'Monday', 'Tuesday']):
        mean1 = self.calculate_mean_change(sched1)
        mean2 = self.calculate_mean_change(sched2)

        t_stat, p_value = stats.ttest_ind(sched1, sched2)

        if p_value < 0.05:
            return f"There is a significant difference between the two sets of days (p={p_value})."
        else:
            return f"There is no significant difference between the two sets of days (p={p_value})."
       
        
    # second hypothesis test question:
    # null hypothesis: The mean volume of three cryptos {'Ethereum', 'Bitcoin', 'USDt Tether'} is significantly more than the mean volume of other cryptos

    def calculate_mean_volume(self, coins):
        volumes = []
        for coin in coins:
            volume = self.db.query(f"SELECT volume FROM coin_history WHERE coin='{coin}'")
            volumes.append(volume)
        return sum(volumes) / len(volumes)
    # This method calculates the mean volume of a given list of coins.
    # It queries the database for the volume of each coin and calculates the mean.

    def compare_volumes(self, top_coins):
        top_coins_volume = self.calculate_mean_volume(top_coins)
        all_coins = self.db.query("SELECT DISTINCT coin FROM coin_history")
        other_coins = [coin for coin in all_coins if coin not in top_coins]
        other_coins_volume = self.calculate_mean_volume(other_coins)
        t_stat, p_value = stats.ttest_ind(top_coins_volume, other_coins_volume)

        if p_value < 0.05:
            return f"The mean volume of {top_coins} is significantly more than the mean volume of other cryptos."
        else:
            return f"The mean volume of {top_coins} is not significantly more than the mean volume of other cryptos."
    # This method compares the mean volume of the list of top coins with the mean volume of other coins.
    # Finally perform t-test to determine if there is a significant difference between two groups or not.     
            
         

