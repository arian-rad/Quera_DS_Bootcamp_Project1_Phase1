# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

# Define a function to download a CSV file
def Download_csv(HistoricalLink):
    try:
        # Initialize a Chrome webdriver
        driver = webdriver.Chrome()
        
        # Open the provided HistoricalLink URL
        driver.get(HistoricalLink)
        
        # Wait for 3 seconds (you may want to adjust this delay)
        time.sleep(3)
        
        # Find and click the button that corresponds to a specific date range
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., '7/7/2023 - 9/8/2023')]"))
        )
        button.click()
        
        # Wait for 3 seconds (you may want to adjust this delay)
        time.sleep(3)
        
        # Select the "Last 365 days" option (if present)
        last_365_days_option = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//li[contains(., 'Last 365 days')]"))
        )
        last_365_days_option.click()
        
        # Find and click the "Continue" button
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Continue']"))
        )
        continue_button.click()
        
        # Wait for 3 seconds (you may want to adjust this delay)
        time.sleep(3)
        
        # Find and click the "Download CSV" button
        button_csv = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Download CSV')]"))
        )
        button_csv.click()
        
        # Wait for 3 seconds (you may want to adjust this delay)
        time.sleep(3)

    except Exception as e:
        print("An error occurred:", str(e))

    finally:
        driver.quit()  # Close the Chrome browser when done
