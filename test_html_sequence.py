import logging
import pandas as pd
from selenium.webdriver.common.by import By

from utils import save_result


def test_html_sequence(driver, url):
    """
    Test to check the presence and sequence of HTML header tags (H1 to H6) on the page.

    Args:
        driver: Selenium WebDriver instance.
        url: URL of the webpage to test.

    Returns:
        DataFrame: Test results as a pandas DataFrame with columns 'tags', 'result', and 'comments'.
    """
    logging.info(f"Starting HTML Sequence Test for URL: {url}")
    testcase = "HTML Tag Sequence Test"

    try:
        # Navigate to the URL
        driver.get(url)
        logging.info("Page loaded successfully.")

        # Generate tags H1 to H6
        tags = [f"h{i}" for i in range(1, 7)]
        logging.debug(f"Generated tag list: {tags}")

        # Find elements for each tag
        elements = {tag: driver.find_elements(By.TAG_NAME, tag) for tag in tags}

        # Check for missing tags
        results = []
        for tag, elems in elements.items():
            if len(elems) == 0:
                results.append({"tags": tag, "result": "Fail", "comments": f"{tag} is missing"})
            else:
                results.append({"tags": tag, "result": "Pass", "comments": f"{tag} is present"})

        # Convert results to a DataFrame
        result_df = pd.DataFrame(results)

        # Save the result
        save_result(result_df, testcase)

        return result_df

    except Exception as e:
        logging.error(f"Error during {testcase}: {str(e)}", exc_info=True)
        error_result = pd.DataFrame([{"tags": "N/A", "result": "Fail", "comments": str(e)}])
        save_result(error_result, testcase)
        return error_result