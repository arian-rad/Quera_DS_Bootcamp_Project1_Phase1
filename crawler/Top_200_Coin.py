# Import necessary libraries
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import re
import csv
import time

# Initialize a Chrome webdriver
driver = webdriver.Chrome()

# Specify the URL you want to scrape
url = "https://coinmarketcap.com/historical/20230825/"

# Open the URL in the Chrome browser
driver.get(url)

# Wait for 5 seconds (you may want to adjust this delay)
time.sleep(5)

# Find and click the "Accept All Cookies" button (if present)
cookie_button = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Accept All Cookies')]"))
)
driver.execute_script("arguments[0].scrollIntoView();", cookie_button)
cookie_button.click()

# Wait for 10 seconds (you may want to adjust this delay)
time.sleep(10)

# Determine the height of the web page for scrolling
scroll_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")

# Specify the scrolling speed
scroll_speed = 15

# Scroll through the entire page in small increments
for i in range(0, scroll_height, scroll_speed):
    driver.execute_script(f"window.scrollTo(0, {i});")
    time.sleep(0.1)

# Wait for 10 seconds (you may want to adjust this delay)
time.sleep(10)

# Parse the HTML content of the page using BeautifulSoup
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Wait for 10 seconds (you may want to adjust this delay)
time.sleep(10)

# Find all table rows with the class 'cmc-table-row'
tr_elements = soup.find_all('tr', class_='cmc-table-row')

# Initialize an empty list to store data from the table
table = []

# Loop through the table rows, extracting relevant data
for tr in tr_elements[0:200]:  # Extract data from a specific row (you can change this)
    rank_div = tr.find('div', class_='')
    symbol_link = tr.find('a', class_='cmc-table__column-name--symbol')

    rank = "N/A"
    symbol = "N/A"
    name_coin = "N/A"
    name_link = "N/A"

    if rank_div:
        rank = rank_div.text.strip()

    if symbol_link:
        symbol = symbol_link.text.strip()

    name_div = tr.find('div', class_='cmc-table__column-name')
    if name_div:
        name_link_elem = name_div.find('a')
        if name_link_elem:
            name_link = name_link_elem.get('href')
            name_coin = name_link_elem.get('title')

    # Create links for historical and main pages
    historical_link = f'https://coinmarketcap.com{name_link}historical-data/'
    main_link = f'https://coinmarketcap.com{name_link}'
    
    # Append data to the table list
    table.append([rank, symbol, name_coin, historical_link, main_link])

# Specify the output CSV file
csv_file = 'coin_data.csv'

# Write data to the CSV file
with open(csv_file, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Rank', 'Symbol', 'Name', 'Historical Link', 'Main Link'])
    csv_writer.writerows(table)

# Print a message confirming that data has been saved to the CSV file
print(f'Data saved to {csv_file}')

# Quit the Chrome browser
driver.quit()
