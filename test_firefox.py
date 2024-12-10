import os
import logging
from dotenv import load_dotenv
from selenium.webdriver.support import expected_conditions as EC

from utils import setup_driver, save_report
from test_h1_tag_existence import test_h1_tag_existence
from test_html_sequence import test_html_sequence
from test_image_alt import test_image_alt
from test_url_status import test_url_status
from test_currency_filter import test_currency_filter
from extract_script_data import extract_script_data


load_dotenv()
# Define WebDriver path
FIREFOX_DRIVER_PATH = os.getenv("FIREFOX_DRIVER_PATH")

logging.basicConfig(
    level=logging.INFO,  # Set the minimum logging level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
    handlers=[
        logging.FileHandler("automation_test.log"),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

# Main Execution
def main():
    url = os.getenv("TEST_URL")
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
            # print(test_results)
        
        # Save the report
        save_report(test_results)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
