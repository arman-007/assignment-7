from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Define the path to the ChromeDriver in your project root
CHROME_DRIVER_PATH = "./chromedriver"  # Adjust the path if necessary

def main():
    # Set up the WebDriver using the Chrome Service
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service)

    try:
        # Open a website (Example: Google)
        driver.get("https://www.google.com")

        # Verify the page title
        # print("Page title is:", driver.title)
        print(driver)

        # Find the search bar using its name attribute and perform a search
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys("Selenium testing with Python")
        search_box.submit()

        # Wait for the results to load and verify a keyword in the results
        driver.implicitly_wait(5)  # Wait up to 5 seconds for elements to appear
        print("Search results page title is:", driver.title)

    except Exception as e:
        print("An error occurred:", e)

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    main()
