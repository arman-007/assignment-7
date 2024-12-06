import os
import time
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

# Define WebDriver path
CHROME_DRIVER_PATH = "./chromedriver"

logging.basicConfig(
    level=logging.INFO,  # Set the minimum logging level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
    handlers=[
        logging.FileHandler("automation_test.log"),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

# Initialize WebDriver
def setup_driver():
    service = Service(CHROME_DRIVER_PATH)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# H1 Tag Test
def test_h1_tag_existence(driver, url):
    try:
        logging.info(f"Navigating to {url}")
        driver.get(url)
        # time.sleep(2)  # Wait for the page to load

        h1_tags = driver.find_elements(By.TAG_NAME, "h1")
        if not h1_tags:
            logging.error(f"H1 tag is missing on page: {url}")
            return {"testcase": "H1 Tag Existence", "result": "Fail", "comments": "H1 tag missing"}
        else:
            logging.info(f"H1 tag found on page: {url}")
            return {"testcase": "H1 Tag Existence", "result": "Pass", "comments": "H1 tag exists"}
    except Exception as e:
        logging.exception(f"An error occurred during the H1 Tag Existence Test: {str(e)}")
        return {"testcase": "H1 Tag Existence", "result": "Fail", "comments": str(e)}

# HTML Tag Sequence Test
def test_html_sequence(driver, url):
    logging.info(f"Starting HTML Sequence Test for URL: {url}")
    testcase = "HTML Tag Sequence Test"
    # print(testcase)
    try:
        # Navigate to the URL
        driver.get(url)
        logging.info("Page loaded successfully.")

        # Generate tags H1 to H6
        tags = [f"h{i}" for i in range(1, 7)]
        logging.debug(f"Generated tag list: {tags}")

        # Find elements for each tag
        elements = [driver.find_elements(By.TAG_NAME, tag) for tag in tags]
        missing = [tags[i] for i in range(len(elements)) if len(elements[i]) == 0]

        # Check for missing tags
        if missing:
            comment = f"Missing tags: {', '.join(missing)}"
            logging.warning(f"{testcase} failed: {comment}")
            return {"testcase": testcase, "result": "Fail", "comments": comment}

        comment = "All H1-H6 tags are sequentially present."
        logging.info(f"{testcase} passed: {comment}")
        return {"testcase": testcase, "result": "Pass", "comments": comment}

    except Exception as e:
        logging.error(f"Error during {testcase}: {str(e)}", exc_info=True)
        return {"testcase": testcase, "result": "Fail", "comments": str(e)}

# Image Alt Attribute Test
def test_image_alt(driver, url):
    """
    Test to verify that all images on the page have 'alt' attributes.

    Args:
        driver (webdriver): Selenium WebDriver instance.
        url (str): URL of the page to test.

    Returns:
        dict: Dictionary containing testcase name, result, and comments.
    """
    logging.info(f"Starting Image Alt Attribute Test for URL: {url}")
    testcase = "Image Alt Attribute Test"

    try:
        # Navigate to the page
        driver.get(url)
        logging.info("Page loaded successfully.")

        # Find all <img> tags on the page
        images = driver.find_elements(By.TAG_NAME, "img")
        print(len(images))
        logging.info(f"Found {len(images)} images on the page.")

        # Check for missing 'alt' attributes
        missing_alt = [img.get_attribute("src") for img in images if not img.get_attribute("alt")]
        if missing_alt:
            comment = f"{len(missing_alt)} images are missing 'alt' attributes."
            logging.warning(f"{testcase} failed: {comment}")
            return {"testcase": testcase, "result": "Fail", "comments": comment}

        # If all images have 'alt' attributes
        comment = "All images have 'alt' attributes."
        logging.info(f"{testcase} passed: {comment}")
        return {"testcase": testcase, "result": "Pass", "comments": comment}

    except Exception as e:
        logging.error(f"Error during {testcase}: {str(e)}", exc_info=True)
        return {"testcase": testcase, "result": "Fail", "comments": str(e)}

# URL Status Code Test
def test_url_status(driver, url):
    """
    Test to verify that all links on the page are valid (not broken).

    Args:
        driver (webdriver): Selenium WebDriver instance.
        url (str): URL of the page to test.

    Returns:
        dict: Dictionary containing testcase name, result, and comments.
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

        # Check the status of each link
        broken_urls = []
        for link in links:
            href = link.get_attribute("href")
            if href:
                try:
                    response = requests.head(href, timeout=5)
                    if response.status_code == 404:
                        logging.warning(f"Broken URL found: {href}")
                        broken_urls.append(href)
                except requests.RequestException as e:
                    logging.error(f"Error checking URL {href}: {str(e)}")
                    broken_urls.append(href)

        # Report results
        if broken_urls:
            comment = f"Broken URLs: {len(broken_urls)}. See logs for details."
            logging.warning(f"{testcase} failed: {comment}")
            return {"testcase": testcase, "result": "Fail", "comments": comment}

        comment = "All URLs are valid."
        logging.info(f"{testcase} passed: {comment}")
        return {"testcase": testcase, "result": "Pass", "comments": comment}

    except Exception as e:
        logging.error(f"Error during {testcase}: {str(e)}", exc_info=True)
        return {"testcase": testcase, "result": "Fail", "comments": str(e)}

# Currency Filter Test
def test_currency_filter(driver, url):
    """
    Test to validate the currency filter functionality on the page.

    Args:
        driver (webdriver): Selenium WebDriver instance.
        url (str): URL of the page to test.

    Returns:
        dict: Dictionary containing testcase name, result, and comments.
    """
    logging.info(f"Starting Currency Filter Test for URL: {url}")
    testcase = "Currency Filter Test"

    try:
        # Navigate to the page
        driver.get(url)
        logging.info("Page loaded successfully.")
        
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "js-currency-sort-footer"))
        )
        # Locate the currency dropdown
        ActionChains(driver).move_to_element(element).perform()
        dropdown = driver.find_element(By.ID, "js-currency-sort-footer")
        dropdown.click()
        logging.info("Currency dropdown opened.")

        # Locate the dropdown options
        options = dropdown.find_elements(By.CSS_SELECTOR, ".select-ul > li")
        logging.info(f"Found {len(options)} currency options.")

        if not options:
            comment = "No currency options found in the dropdown."
            logging.warning(f"{testcase} failed: {comment}")
            return {"testcase": testcase, "result": "Fail", "comments": comment}

        # Iterate through each currency option
        for option in options:
            # Scroll to the option to make it visible and click
            ActionChains(driver).move_to_element(option).perform()
            option.click()
            time.sleep(2)  # Wait for the page to update

            # Extract the currency symbol from the selected option
            currency_symbol = option.find_element(By.TAG_NAME, "p").text()#.text.split(" ")[0]
            logging.info(f"Testing currency: {currency_symbol}")

            # Validate that the currency symbol is displayed in property tiles
            tiles = driver.find_elements(By.CLASS_NAME, "property-tile")  # Adjust class name if necessary
            if not tiles:
                comment = "No property tiles found on the page."
                logging.warning(f"{testcase} failed: {comment}")
                return {"testcase": testcase, "result": "Fail", "comments": comment}

            if not all(currency_symbol in tile.text for tile in tiles):
                comment = f"Currency symbol {currency_symbol} not found in all property tiles."
                logging.warning(f"{testcase} failed: {comment}")
                return {"testcase": testcase, "result": "Fail", "comments": comment}

        # If all currency options pass the validation
        comment = "Currency filter working correctly for all options."
        logging.info(f"{testcase} passed: {comment}")
        return {"testcase": testcase, "result": "Pass", "comments": comment}

    except Exception as e:
        logging.error(f"Error during {testcase}: {str(e)}", exc_info=True)
        return {"testcase": testcase, "result": "Fail", "comments": str(e)}

# Script Data Extraction
def extract_script_data(driver, url):
    driver.get(url)
    try:
        script = driver.find_element(By.TAG_NAME, "script")
        script_data = script.get_attribute("innerHTML")
        return script_data  # Process and parse as required
    except Exception as e:
        return str(e)

# Save Report
def save_report(test_results):
    # Define the directory and file path
    directory = "reports"
    file_path = os.path.join(directory, "test_report.csv")

    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Save the results to a CSV file
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
            ("Currency Filter Test", test_currency_filter)
        ]
        
        for name, test in tests:
            # print(test(driver, url))
            result = test(driver, url)
            # print(result)
            test_results.append(result)
            print(test_results)
        
        # Save the report
        save_report(test_results)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
