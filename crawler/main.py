# Import necessary libraries
import subprocess
import csv
import json
import time
from Save_Tags_GithubLink import Save_Tags  # Assuming you have a Save_Tags function in the Save_Tags module
from Historic_Coin_CSV import Download_csv  # Assuming you have a Download_csv function in the Download_csv module

try:
    # Run the Top_coins.py script using subprocess
    subprocess.run(["/usr/local/bin/python3.8", "Top_coins.py"])
    
    # Wait for 5 seconds (you may want to adjust this delay)
    time.sleep(5)

    table = []  # Initialize an empty list to store data
    all_tag_data = {}  # Initialize a dictionary to store tag data
    all_github_data = {}  # Initialize a dictionary to store GitHub data
    error_data = {}  # Initialize a dictionary to store error data

    # Open the coin_data.csv file for reading
    with open("coin_data.csv", "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Iterate over each row in the CSV file
        for row in reader:
            historical_link = row["Historical Link"]  # Get the historical link
            main_link = row["Main Link"]  # Get the main link
            
            try:
                # Call the Save_Tags function to extract tag and GitHub data
                tag_data, github_data, error_coin = Save_Tags(main_link)
                
                # Store the tag and GitHub data in dictionaries
                all_tag_data[main_link] = tag_data
                all_github_data[main_link] = github_data

            except Exception as e:
                print(f"Error processing {main_link}: {e}")
                error_data[main_link] = str(e)

            # Call the Download_csv function to download CSV data from the historical link
            Download_csv(historical_link)

    # Save the collected tag data to a JSON file
    with open("all_tag_data.json", "w") as tag_data_file:
        json.dump(all_tag_data, tag_data_file)

    # Save the collected GitHub data to a JSON file
    with open("all_github_data.json", "w") as github_data_file:
        json.dump(all_github_data, github_data_file)

    # Save the error data to a JSON file
    with open("error_data.json", "w") as error_data_file:
        json.dump(error_data, error_data_file)

except Exception as e:
    print(f"An error occurred: {e}")
