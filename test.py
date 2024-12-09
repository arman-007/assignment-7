import os
import time
import json
import logging
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Dict, Any


CHROME_DRIVER_PATH = "./chromedriver"

logging.basicConfig(
    level=logging.INFO,  # Set the minimum logging level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
    handlers=[
        logging.FileHandler("automation_test.log"),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

def setup_driver():
    service = Service(CHROME_DRIVER_PATH)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    return driver

def extract_script_data(driver, url):
    """
    Extract data from the JavaScript script tag or window object on the page and save it to a report.

    Args:
        driver (webdriver): Selenium WebDriver instance.
        url (str): URL of the page to test.

    Returns:
        dict: Dictionary containing testcase name, result, and comments.
    """
    logging.info(f"Starting Script Data Extraction for URL: {url}")
    testcase = "Script Data Extraction Test"

    try:
        # Navigate to the page
        driver.get(url)
        logging.info("Page loaded successfully.")
        
        # Wait until the page is fully loaded
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Extract ScriptData from the JavaScript context (using window object or other method)
        script_data = driver.execute_script("return window.ScriptData;")  # Modify this as needed

        if not script_data:
            logging.warning("Script data not found on the page.")
            return {"testcase": testcase, "result": "Fail", "comments": "Script data not found."}

        extracted_data = {
            "SiteURL": script_data["config"]["SiteUrl"],
            "CampaignID": script_data["pageData"]["CampaignId"],  # Example key from the script data
            "SiteName": script_data["config"]["SiteName"],  # Example key
            "Browser": script_data["userInfo"]["Browser"],  # Example key
            "Country": script_data["userInfo"]["CountryCode"],  # Example key
            "IP" : script_data["userInfo"]["IP"]
        }
        return {"testcase": testcase, "result": "Pass", "comments": extracted_data}
    
    except Exception as e:
        logging.error(f"Error during Script Data Extraction: {e}")
        return {"testcase": testcase, "result": "Fail", "comments": f"Error: {e}"}

# Save Report
def save_report(test_results):
    # Define the directory and file path
    directory = "reports"
    file_path = os.path.join(directory, "test_report.csv")

    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Save the results to a CSV file
    print(test_results)
    df = pd.DataFrame(test_results)
    df.to_csv(file_path, index=False)

    print(f"Report saved at {file_path}")


# Main Execution
def main():
    url = "https://www.alojamiento.io/property/apartamentos-centro-col%c3%b3n/BC-189483"
    driver = setup_driver()
    test_results = []

    try:
        # Execute tests
        tests = [
            # ("H1 Tag Test", test_h1_tag_existence),
            # ("HTML Sequence Test", test_html_sequence),
            # ("Image Alt Test", test_image_alt),
            # ("URL Status Code Test", test_url_status),
            # ("Currency Filter Test", test_currency_filter),
            ("Scrape data from script data", extract_script_data),
        ]
        
        for name, test in tests:
            result = test(driver, url)
            test_results.append(result)
            print(test_results)

        # Save the report
        save_report(test_results)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()