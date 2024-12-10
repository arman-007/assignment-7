import logging
import pandas as pd
from selenium.webdriver.common.by import By

from utils import save_result


# def test_image_alt(driver, url):
#     """
#     Test to verify that all images on the page have 'alt' attributes.

#     Args:
#         driver (webdriver): Selenium WebDriver instance.
#         url (str): URL of the page to test.

#     Returns:
#         dict: Dictionary containing testcase name, result, and comments.
#     """
#     logging.info(f"Starting Image Alt Attribute Test for URL: {url}")
#     testcase = "Image Alt Attribute Test"

#     try:
#         # Navigate to the page
#         driver.get(url)
#         logging.info("Page loaded successfully.")

#         # Find all <img> tags on the page
#         images = driver.find_elements(By.TAG_NAME, "img")
#         logging.info(f"Found {len(images)} images on the page.")

#         # Check for missing 'alt' attributes
#         missing_alt = [img.get_attribute("src") for img in images if not img.get_attribute("alt")]
#         if missing_alt:
#             comment = f"{len(missing_alt)} images are missing 'alt' attributes."
#             logging.warning(f"{testcase} failed: {comment}")
#             return {"testcase": testcase, "result": "Fail", "comments": comment}

#         # If all images have 'alt' attributes
#         comment = "All images have 'alt' attributes."
#         logging.info(f"{testcase} passed: {comment}")
#         return {"testcase": testcase, "result": "Pass", "comments": comment}

#     except Exception as e:
#         logging.error(f"Error during {testcase}: {str(e)}", exc_info=True)
#         return {"testcase": testcase, "result": "Fail", "comments": str(e)}


def test_image_alt(driver, url):
    """
    Test to verify that all images on the page have 'alt' attributes.

    Args:
        driver: Selenium WebDriver instance.
        url: URL of the page to test.

    Returns:
        DataFrame: Test results as a pandas DataFrame with columns 'src', 'result', and 'alt'.
    """
    logging.info(f"Starting Image Alt Attribute Test for URL: {url}")
    testcase = "Image Alt Attribute Test"

    try:
        # Navigate to the page
        driver.get(url)
        logging.info("Page loaded successfully.")

        # Find all <img> tags on the page
        images = driver.find_elements(By.TAG_NAME, "img")
        logging.info(f"Found {len(images)} images on the page.")

        # Prepare results for each image
        results = []
        for img in images:
            src = img.get_attribute("src")
            alt = img.get_attribute("alt")
            if alt:
                result = "Pass"
                comments = alt
            else:
                result = "Fail"
                comments = "Missing 'alt' attribute"
            results.append({"src": src, "result": result, "alt": comments})

        # Convert results to a DataFrame
        result_df = pd.DataFrame(results)

        # Save the result
        save_result(result_df, testcase)

        return result_df

    except Exception as e:
        logging.error(f"Error during {testcase}: {str(e)}", exc_info=True)
        error_result = pd.DataFrame([{"src": "N/A", "result": "Fail", "alt": str(e)}])
        save_result(error_result, testcase)
        return error_result