import logging
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import save_result


def extract_script_data(driver, url):
    """
    Extract data from the JavaScript script tag or window object on the page and save it to a report.

    Args:
        driver (webdriver): Selenium WebDriver instance.
        url (str): URL of the page to test.

    Returns:
        DataFrame: Extracted script data as a pandas DataFrame with specific columns.
    """
    logging.info(f"Starting Script Data Extraction for URL: {url}")
    testcase = "Script Data Extraction Test"

    try:
        # Navigate to the page
        driver.get(url)
        logging.info("Page loaded successfully.")
        
        # Wait until the page is fully loaded
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Extract ScriptData from the JavaScript context
        script_data = driver.execute_script("return window.ScriptData;")  # Modify as needed

        if not script_data:
            logging.warning("Script data not found on the page.")
            return pd.DataFrame([{
                "SiteURL": "N/A", "CampaignID": "N/A", "SiteName": "N/A",
                "Browser": "N/A", "Country": "N/A", "IP": "N/A", "result": "Fail",
                "comment": "Script data not found."
            }])

        # Parse and structure the data
        extracted_data = {
            "SiteURL": script_data["config"].get("SiteUrl", "N/A"),
            "CampaignID": script_data["pageData"].get("CampaignId", "N/A"),
            "SiteName": script_data["config"].get("SiteName", "N/A"),
            "Browser": script_data["userInfo"].get("Browser", "N/A"),
            "Country": script_data["userInfo"].get("CountryCode", "N/A"),
            "IP": script_data["userInfo"].get("IP", "N/A"),
            # "result": "Pass",
            # "comment": "Data extracted successfully."
        }

        # Convert to DataFrame
        result_df = pd.DataFrame([extracted_data])

        # Save the result
        save_result(result_df, testcase)

        return result_df

    except Exception as e:
        logging.error(f"Error during Script Data Extraction: {e}")
        error_data = {
            "SiteURL": "N/A", "CampaignID": "N/A", "SiteName": "N/A",
            "Browser": "N/A", "Country": "N/A", "IP": "N/A", "result": "Fail",
            "comment": f"Error: {e}"
        }
        error_df = pd.DataFrame([error_data])
        save_result(error_df, testcase)
        return error_df