import os
import json
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
        # logging.StreamHandler()  # Log to the console
    ]
)

# Initialize WebDriver
def setup_driver():
    service = Service(CHROME_DRIVER_PATH)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
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
        
        # Wait for the page to load completely
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Scroll to the bottom of the page multiple times to ensure lazy-loaded content is visible
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Allow time for any lazy-loaded content to appear
        
        # Additional wait to ensure page is fully interactive
        time.sleep(3)

        # Try to find and click the currency dropdown with multiple attempts
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                # Scroll to the bottom again before each attempt
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                # Wait and attempt to find the dropdown
                dropdown = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "js-currency-sort-footer"))
                )
                
                # Try to click the dropdown
                # dropdown.click()
                # logging.info("Currency dropdown opened.")
                
                # If successful, break the loop
                break
            
            except Exception as click_error:
                logging.warning(f"Dropdown click attempt {attempt + 1} failed: {click_error}")
                
                # If it's the last attempt, raise the exception
                if attempt == max_attempts - 1:
                    raise

        # Locate the dropdown options once
        options = dropdown.find_elements(By.CSS_SELECTOR, ".select-ul > li")
        logging.info(f"Found {len(options)} currency options.")

        # Parse dropdown options into a structured list
        currency_options = []
        for option in options:
            data_country = option.get_attribute("data-currency-country")
            currency_element = option.find_element(By.CSS_SELECTOR, ".option > p")
            currency_symbol = currency_element.text.split(" ")[0].strip()
            currency_options.append({"country": data_country, "symbol": currency_symbol})
            logging.info(f"Currency option: {data_country} -> {currency_symbol}")

        if not currency_options:
            comment = "No currency options found in the dropdown."
            logging.warning(f"{testcase} failed: {comment}")
            return {"testcase": testcase, "result": "Fail", "comments": comment}

        # Loop through all currency options and select each one
        for currency in currency_options:
            logging.info(f"Selecting currency: {currency['country']} -> {currency['symbol']}")

            # Reopen the dropdown before each selection with multiple attempts
            for attempt in range(max_attempts):
                try:
                    # Scroll to the bottom of the page
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                    # Wait until the currency dropdown is clickable
                    dropdown = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "js-currency-sort-footer"))
                    )

                    # Click the dropdown to open it
                    dropdown.click()
                    logging.info("Currency dropdown opened.")
                    
                    # Break the loop if successful
                    break
                
                except Exception as retry_error:
                    logging.warning(f"Dropdown reopen attempt {attempt + 1} failed: {retry_error}")
                    
                    # If it's the last attempt, raise the exception
                    if attempt == max_attempts - 1:
                        raise

            # Locate the option based on the country
            option = next(
                (opt for opt in options if opt.get_attribute("data-currency-country") == currency["country"]), None
            )
            if not option:
                logging.warning(f"Option for {currency['country']} not found.")
                continue

            # Scroll the option into view and wait for it to be clickable
            driver.execute_script("arguments[0].scrollIntoView();", option)
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(option)
            ).click()

            # Wait a bit for the page to update
            time.sleep(2)  # Adjust this time if necessary

            # Validate that the currency symbol is displayed in property tiles
            tiles = driver.find_elements(By.CLASS_NAME, "js-price-value")  # Adjust class name if necessary         
            if not tiles:
                comment = f"No property tiles found after selecting {currency['symbol']}."
                logging.warning(f"{testcase} failed: {comment}")
                return {"testcase": testcase, "result": "Fail", "comments": comment}
            
            logging.info(f"There are {len(tiles)} property tiles.")

            if not all(currency["symbol"] in tile.text for tile in tiles):
                comment = f"Currency symbol {currency['symbol']} not found in all property tiles."
                logging.warning(f"{testcase} failed: {comment}")
                return {"testcase": testcase, "result": "Fail", "comments": comment}

            logging.info(f"Currency {currency['symbol']} validated successfully.")
        
        return {"testcase": testcase, "result": "Pass", "comments": "All currency options validated successfully."}
    
    except Exception as e:
        logging.error(f"Error during Currency Filter Test: {str(e)}")
        return {"testcase": testcase, "result": "Fail", "comments": str(e)}

# Script Data Extraction
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
    # Define the directory and file path for the Excel report
    directory = "reports"
    file_path = os.path.join(directory, "test_report.xlsx")

    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Prepare the data for the Excel report
    formatted_results = []
    
    for result in test_results:
        # Extract the 'testcase', 'result', and 'comments'
        testcase = result['testcase']
        test_result = result['result']
        
        # Check if comments are a dictionary or a string
        comments = result['comments']
        
        # If comments are a dictionary, convert it to a string for easier viewing
        if isinstance(comments, dict):
            comments = "; ".join([f"{key}: {value}" for key, value in comments.items()])
        
        # Append the formatted data as a row
        formatted_results.append({
            'testcase': testcase,
            'result': test_result,
            'comments': comments
        })
    
    # Create a DataFrame from the formatted results
    df = pd.DataFrame(formatted_results)

    # Save the DataFrame to an Excel file
    df.to_excel(file_path, index=False, engine='openpyxl')

    print(f"Report saved at {file_path}")

# Main Execution
def main():
    url = "https://www.alojamiento.io/property/apartamentos-centro-col%c3%b3n/BC-189483"
    driver = setup_driver()
    test_results = []

    try:
        # Execute tests
        tests = [
            ("H1 Tag Test", test_h1_tag_existence),
            ("HTML Sequence Test", test_html_sequence),
            ("Image Alt Test", test_image_alt),
            ("URL Status Code Test", test_url_status),
            ("Currency Filter Test", test_currency_filter),
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
