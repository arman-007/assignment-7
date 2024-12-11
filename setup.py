import os
import pandas as pd
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService


load_dotenv()
# CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH")
# FIREFOX_DRIVER_PATH = os.getenv("FIREFOX_DRIVER_PATH")


def get_chrome_driver(headless=False):
    """Set up and return a Chrome WebDriver."""
    # service = ChromeService(CHROME_DRIVER_PATH)
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")  # Run Chrome in headless mode
        options.add_argument("--no-sandbox")  # Required for running as root in Docker
        options.add_argument("--disable-dev-shm-usage")  # Prevents /dev/shm issues
        options.add_argument("--disable-gpu")  # Optional: Disable GPU acceleration
        options.add_argument("--window-size=1920,1080")  # Set a large window size for headless mode
        options.add_argument("--remote-debugging-port=9222")  # Enable remote debugging
    # driver = webdriver.Chrome(service=service, options=options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    return driver


def get_firefox_driver(headless=False):
    """Set up and return a Firefox WebDriver."""

    # Create tmp_dir
    temp_dir = "~/_tmp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    os.environ["TMPDIR"] = temp_dir

    # service = FirefoxService(FIREFOX_DRIVER_PATH)
    options = webdriver.FirefoxOptions()
    if headless:
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080") 
    # driver = webdriver.Firefox(service=service, options=options)
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    driver.maximize_window()
    return driver


def setup_driver(browser="chrome", headless=False):
    """
    Set up the WebDriver based on the specified browser.

    Args:
        browser (str): Browser to use ("chrome" or "firefox").

    Returns:
        WebDriver: Selenium WebDriver instance.
    """
    if browser.lower() == "chrome":
        return get_chrome_driver(headless)
    elif browser.lower() == "firefox":
        return get_firefox_driver(headless)
    else:
        raise ValueError(f"Unsupported browser: {browser}. Use 'chrome' or 'firefox'.")

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