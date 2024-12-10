import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
            "CampaignID": script_data["pageData"]["CampaignId"],
            "SiteName": script_data["config"]["SiteName"],
            "Browser": script_data["userInfo"]["Browser"],
            "Country": script_data["userInfo"]["CountryCode"],
            "IP" : script_data["userInfo"]["IP"]
        }
        return {"testcase": testcase, "result": "Pass", "comments": extracted_data}
    
    except Exception as e:
        logging.error(f"Error during Script Data Extraction: {e}")
        return {"testcase": testcase, "result": "Fail", "comments": f"Error: {e}"}