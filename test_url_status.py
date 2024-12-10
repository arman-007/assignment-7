import logging
import requests
import pandas as pd
from selenium.webdriver.common.by import By

from utils import save_result


# def test_url_status(driver, url):
#     """
#     Test to verify that all links on the page are valid (not broken).

#     Args:
#         driver (webdriver): Selenium WebDriver instance.
#         url (str): URL of the page to test.

#     Returns:
#         dict: Dictionary containing testcase name, result, and comments.
#     """
#     logging.info(f"Starting URL Status Test for URL: {url}")
#     testcase = "URL Status Test"

#     try:
#         # Navigate to the page
#         driver.get(url)
#         logging.info("Page loaded successfully.")

#         # Find all anchor (<a>) tags on the page
#         links = driver.find_elements(By.TAG_NAME, "a")
#         logging.info(f"Found {len(links)} links on the page.")

#         # Check the status of each link
#         broken_urls = []
#         for link in links:
#             href = link.get_attribute("href")
#             if href:
#                 try:
#                     response = requests.head(href, timeout=5)
#                     if response.status_code == 404:
#                         logging.warning(f"Broken URL found: {href}")
#                         broken_urls.append(href)
#                 except requests.RequestException as e:
#                     logging.error(f"Error checking URL {href}: {str(e)}")
#                     broken_urls.append(href)

#         # Report results
#         if broken_urls:
#             comment = f"Broken URLs: {len(broken_urls)}. See logs for details."
#             logging.warning(f"{testcase} failed: {comment}")
#             return {"testcase": testcase, "result": "Fail", "comments": comment}

#         comment = "All URLs are valid."
#         logging.info(f"{testcase} passed: {comment}")
#         return {"testcase": testcase, "result": "Pass", "comments": comment}

#     except Exception as e:
#         logging.error(f"Error during {testcase}: {str(e)}", exc_info=True)
#         return {"testcase": testcase, "result": "Fail", "comments": str(e)}


def test_url_status(driver, url):
    """
    Test to verify that all links on the page are valid (not broken).

    Args:
        driver: Selenium WebDriver instance.
        url: URL of the page to test.

    Returns:
        DataFrame: Test results as a pandas DataFrame with columns 'url', 'result', and 'comments'.
    """
    logging.info(f"Starting URL Status Test for URL: {url}")
    testcase = "URL Status Test"

    try:
        # Navigate to the page
        driver.get(url)
        logging.info("Page loaded successfully.")

        # Find all anchor (<a>) tags on the page
        links = driver.find_elements(By.TAG_NAME, "a")
        logging.info(f"Found {len(links)} links on the page.")

        # Prepare results for each URL
        results = []
        for link in links:
            href = link.get_attribute("href")
            if href:
                try:
                    # Make a HEAD request to check the URL
                    response = requests.head(href, timeout=5)
                    if response.status_code == 404:
                        result = "Fail"
                        comments = "404 Not Found"
                        logging.warning(f"Broken URL found: {href}")
                    else:
                        result = "Pass"
                        comments = f"Status Code: {response.status_code}"
                except requests.RequestException as e:
                    result = "Fail"
                    comments = f"Error: {str(e)}"
                    logging.error(f"Error checking URL {href}: {str(e)}")
            else:
                result = "Fail"
                comments = "No href attribute"
            
            # Append the result
            results.append({"url": href, "result": result, "comments": comments})

        # Convert results to a DataFrame
        result_df = pd.DataFrame(results)

        # Save the result
        save_result(result_df, testcase)

        return result_df

    except Exception as e:
        logging.error(f"Error during {testcase}: {str(e)}", exc_info=True)
        error_result = pd.DataFrame([{"url": "N/A", "result": "Fail", "comments": str(e)}])
        save_result(error_result, testcase)
        return error_result