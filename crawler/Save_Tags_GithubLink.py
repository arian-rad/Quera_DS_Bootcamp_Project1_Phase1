# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException

# Define a function to extract data
def Save_Tags(MainLink):
    error_coin = []  # Initialize a list to store error coins
    github_data = {}  # Initialize dictionary to store GitHub data
    coin_name = None  # Initialize coin_name variable

    try:
        # Initialize a Chrome webdriver
        driver = webdriver.Chrome()
        driver.get(MainLink)  # Open the provided URL
        time.sleep(8)  # Wait for the page to load
        
        # Scroll down the page to load more content (adjust as needed)
        scroll_down_script = "window.scrollBy(0, 170);" 
        driver.execute_script(scroll_down_script)
        
        # Find and click the "Accept All Cookies" button (if present)
        cookie_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept All Cookies')]"))
        )
        cookie_button.click()
        
        # Find the coin name element and extract the text
        coin_name_element = driver.find_element(By.CSS_SELECTOR, 'span[data-role="coin-name"]')
        coin_name = coin_name_element.text
        
        # Try to find and extract the GitHub link (if present)
        try:
            github_link_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'github.com')]"))
            )
            github_link = driver.execute_script("return arguments[0].getAttribute('href');", github_link_element)
            if github_link:
                github_data = {f"{coin_name}_GitHub_Link": github_link}
        except Exception as github_exception:
            # Handle the case where the GitHub link is not found
            github_data = {f"{coin_name}_GitHub_Link": "null"}
        
        # Try to expand the "Show all" section and extract tag values
        try:
            span = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(., 'Show all')]"))
            )
            span.click()
            time.sleep(5)  # Wait for the tags to load
            
            # Find all 'a' elements within a specific CSS selector
            a_elements = driver.find_elements(By.CSS_SELECTOR, '.sc-16891c57-0.sc-9ee74f67-0.iGa-diC a.cmc-link')
            span_values = [a.text for a in a_elements]
            tag_data = {f"{coin_name}_Tags": span_values}
        except TimeoutException:
            # If "Show all" is not present, extract tag values from an alternative location
            div_element = driver.find_element(By.CSS_SELECTOR, 'div.sc-16891c57-0.itVAyl.coin-tags[data-role="stats-block"]')
            a_elements = div_element.find_elements(By.CSS_SELECTOR, 'div.sc-16891c57-0.gPFIPZ span.sc-16891c57-0.sc-9ee74f67-1.dWtIZr a.cmc-link')
            values = [a.text for a in a_elements]
            tag_data = {f"{coin_name}_Tags": values}
                
        return tag_data, github_data, error_coin

    except Exception as e:
        print("An error occurred:", str(e))
        if coin_name:
            error_coin.append(coin_name)
    finally:
        driver.quit()  # Close the browser when done
