import pandas as pd
import statistics as stats

#Load the dataset
data = pd.read_csv("")

#Convert the date column to a datetime object
data['date'] = pd.to_datetime(data['date'])

#Extract the day of the week as a new column
data['day_of_week'] = data['date'].dt.day_name()

#Define two schedules to compare
sched1 = ['Thursday', 'Friday', 'Saturday']
sched2 = ['Sunday', 'Monday', 'Tuesday']

#Calculate the mean change in price for each set of days
mean1 = data[data['day_of_week'].isin(sched1)]['volume'].mean() #not sure about volume!
mean2 = data[data['day_of_week'].isin(sched2)]['volume'].mean()

#assume there is no significant difference between two sets of days.
# null hypothesis states as H0: mean1 = mean2

# Perform a t-test
t_stat, p_value = stats.ttest_ind(sched1, sched2)

# Compare the p-value to the significance level
if p_value < 0.05:
    print(f"There is a significant difference between the two sets of days (p={p_value}).")
else:
    print(f"There is no significant difference between the two sets of days (p={p_value}).")
