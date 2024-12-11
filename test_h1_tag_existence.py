import logging
import pandas as pd
from selenium.webdriver.common.by import By

from utils import save_result

    
def test_h1_tag_existence(driver, url):
    """
    Test to check the existence of an H1 tag on the page.

    Args:
        driver: Selenium WebDriver instance.
        url: URL of the webpage to test.

    Returns:
        DataFrame: Test result as a pandas DataFrame with columns 'testcase', 'result', and 'comments'.
    """
    try:
        logging.info(f"Navigating to {url}")
        driver.get(url)

        h1_tags = driver.find_elements(By.TAG_NAME, "h1")
        if not h1_tags:
            logging.error(f"H1 tag is missing on page: {url}")
            result = {"testcase": "H1 Tag Existence", "result": "Fail", "comments": "H1 tag missing"}
        else:
            logging.info(f"H1 tag found on page: {url}")
            result = {"testcase": "H1 Tag Existence", "result": "Pass", "comments": "H1 tag exists"}
        
        # Convert result to DataFrame
        result_df = pd.DataFrame([result])
        
        # Save the result
        save_result(result_df, "H1 Tag Existence")
        
        return result_df
    
    except Exception as e:
        logging.exception(f"An error occurred during the H1 Tag Existence Test: {str(e)}")
        result = {"testcase": "H1 Tag Existence", "result": "Fail", "comments": str(e)}
        result_df = pd.DataFrame([result])
        save_result(result_df, "H1 Tag Existence")
        return result_df