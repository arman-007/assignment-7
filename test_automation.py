import os
import argparse
import logging
from selenium.webdriver.support import expected_conditions as EC

from setup import setup_driver
from utils import save_result
from test_h1_tag_existence import test_h1_tag_existence
from test_html_sequence import test_html_sequence
from test_image_alt import test_image_alt
from test_url_status import test_url_status
from test_currency_filter import test_currency_filter
from extract_script_data import extract_script_data


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
    """Main function to parse arguments and execute tests."""

    # Browser argument
    parser = argparse.ArgumentParser(description="Run browser-based automation tests.")
    parser.add_argument(
        "--browser",
        type=str,
        default="chrome",
        help="Specify the browser to use: 'chrome' (default) or 'firefox'."
    )

    # Headless argument
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run the tests in headless mode."
    )

    args = parser.parse_args()


    url = os.getenv("TEST_URL")
    driver = setup_driver(browser=args.browser, headless=args.headless)
    # test_results = []

    try:
        # Execute tests
        tests = [
            ("H1 Tag Test", test_h1_tag_existence),
            # ("HTML Sequence Test", test_html_sequence),
            # ("Image Alt Test", test_image_alt),
            # ("URL Status Code Test", test_url_status),
            # ("Currency Filter Test", test_currency_filter),
            # ("Scrape data from script data", extract_script_data),
        ]
        
        for name, test in tests:
            result = test(driver, url)
            # test_results.append(result)
            # print(test_results)
        
        # Save the report
        # save_report(test_results)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
