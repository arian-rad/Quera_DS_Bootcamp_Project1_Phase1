from scipy import stats
import pandas as pd
import numpy as np

#read cryptos from csv file 
coins = pd.read_csv("")

#read the main dataset(365 days behaviour of 200 cryptos)
data = pd.read("")

#get forty random coins from coins
forty_samples = np.random(data, 40)

#get sample's data
sample_data = data[data['Name'] == coins['Name']]

#calculate the mean of the sample as mean_vol and population std as sigma
mean_vol = np.mean(sample_data.volume)
sigma = stats.sem(data.volume)

#calculate the interval for 98% confidence level
confidence = 0.98

z = stats.norm.ppf(1 - (1 - confidence) / 2)
margin_of_error = z * sigma / np.sqrt(40)
ci_lower, ci_upper = sigma - margin_of_error, mean_vol + margin_of_error

print(f"The {confidence*100}% confidence interval is ({ci_lower}, {ci_upper})")
