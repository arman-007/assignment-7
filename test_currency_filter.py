import logging
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import save_result


def test_currency_filter(driver, url):
    """
    Test to validate the currency filter functionality on the page.

    Args:
        driver (webdriver): Selenium WebDriver instance.
        url (str): URL of the page to test.

    Returns:
        DataFrame: Test results as a pandas DataFrame with columns 'currency', 'result', and 'comment'.
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
        
        # Try to find and click the currency dropdown
        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "js-currency-sort-footer"))
        )
        dropdown.click()
        logging.info("Currency dropdown opened.")

        # Locate the dropdown options
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

        dropdown.click()
        if not currency_options:
            comment = "No currency options found in the dropdown."
            logging.warning(f"{testcase} failed: {comment}")
            return pd.DataFrame([{"currency": "N/A", "result": "Fail", "comment": comment}])

        # Prepare results
        results = []

        # Loop through all currency options and select each one
        for currency in currency_options:
            logging.info(f"Selecting currency: {currency['country']} -> {currency['symbol']}")

            # Reopen the dropdown
            dropdown = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "js-currency-sort-footer"))
            )
            dropdown.click()
            logging.info("Currency dropdown reopened.")

            # Locate the option based on the country
            option = next(
                (opt for opt in options if opt.get_attribute("data-currency-country") == currency["country"]), None
            )
            if not option:
                comment = f"Option for {currency['country']} not found."
                logging.warning(comment)
                results.append({"currency": f"{currency["symbol"]} {currency['country']}", "result": "Fail", "comment": comment})
                continue

            # Scroll the option into view and click
            driver.execute_script("arguments[0].scrollIntoView();", option)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(option)).click()

            # Wait a bit for the page to update
            time.sleep(2)

            # Validate that the currency symbol is displayed in property tiles
            tiles = driver.find_elements(By.CLASS_NAME, "js-price-value")  # Adjust class name if necessary
            if not tiles:
                comment = f"No property tiles found after selecting {currency['symbol']} {currency['country']}."
                logging.warning(comment)
                results.append({"currency": f"{currency["symbol"]} {currency['country']}", "result": "Fail", "comment": comment})
                continue
            
            if not all(currency["symbol"] in tile.text for tile in tiles):
                comment = f"Currency symbol {currency['symbol']} {currency['country']} not found in all property tiles."
                logging.warning(comment)
                results.append({"currency": f"{currency["symbol"]} {currency['country']}", "result": "Fail", "comment": comment})
                continue

            # If successful
            comment = f"Currency {currency['symbol']} {currency['country']} validated successfully."
            logging.info(comment)
            results.append({"currency": f"{currency["symbol"]} {currency['country']}", "result": "Pass", "comment": comment})

        # Convert results to a DataFrame
        result_df = pd.DataFrame(results)

        print(result_df)

        # Save the result
        save_result(result_df, testcase)

        return result_df

    except Exception as e:
        logging.error(f"Error during Currency Filter Test: {str(e)}", exc_info=True)
        error_result = pd.DataFrame([{"currency": "N/A", "result": "Fail", "comment": str(e)}])
        save_result(error_result, testcase)
        return error_result