# Vacation Rental Automation Testing

## Overview
This project automates the testing of a vacation rental website to validate essential elements and functionality. The automation script is built using Python, Selenium, and Pandas. The project covers SEO-impact tests, currency filter functionality, and script data extraction, saving results in an Excel report for review.

## Features
- **H1 Tag Existence Test**: Validates the presence of an H1 tag on the page.
- **HTML Tag Sequence Test**: Checks if the HTML header tags (H1 to H6) follow proper sequence without missing tags.
- **Image Alt Attribute Test**: Ensures all images have valid `alt` attributes.
- **URL Status Code Test**: Verifies that all URLs on the page return a valid status (not 404).
- **Currency Filter Test**: Tests the currency filter functionality by validating currency changes in property tiles.
- **Script Data Extraction**: Extracts data from the JavaScript `ScriptData` object for additional insights like SiteURL, CampaignID, SiteName, and more.

## Requirements
### Tools and Libraries
- **Python**: Version 3.10+
- **Libraries**:
  - Selenium
  - Pandas
  - openpyxl
  - Chrome WebDriver

### Browser
- Google Chrome (latest version) with ChromeDriver

### Test Site URL
The project targets the website: [https://www.alojamiento.io](https://www.alojamiento.io)

## Installation
1. **Clone the Repository**
   ```bash
   git clone https://github.com/arman-007/assignment-7.git
   cd assignment-7
   ```

2. **Set up Virtual Environment**
   ```bash
   python -m venv env
   source env/bin/activate   # On Windows: env\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Downloading and Setting Up ChromeDriver**

#### 1. Go to the ChromeDriver Download page.
- Download the Chrome Driver with the same version as your updated Chrome.
- Click the link on the Chrome for Testing availability dashboard: [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)
- [https://googlechromelabs.github.io/chrome-for-testing/](https://googlechromelabs.github.io/chrome-for-testing/) to find the Chrome Driver matching your updated Chrome version.

#### 2. Download the ChromeDriver.
- Download the Chrome Driver version that matches your Chrome.
- [https://googlechromelabs.github.io/chrome-for-testing/](https://googlechromelabs.github.io/chrome-for-testing/)
```
For General Linux distributions, download linux64.
- For Chrome version: https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.141/linux64/chromedriver-linux64.zip
```
- or paste this URL in your browser's search bar
```bash
https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.87/linux64/chromedriver-linux64.zip
```

#### 3. Install the ChromeDriver.
- Since Chrome Driver is a binary file, there is no separate installation process.
- Extract the zip archive and copy the chromedriver file to the directory where Chrome Driver should be located.

#### 4. Make the WebDriver executable.
- Place the WebDriver in the project root and ensure it's executable (For Chrome):
```bash
chmod +x ./chromedriver
```

5. **Set Up .env File**
   - This project uses environment variables to configure settings. Create a .env file in the root directory of the     project and provide the following keys:
     ```env
     CHROME_DRIVER_PATH=./chromedriver
     TEST_URL=https://www.alojamiento.io/property/apartamentos-centro-col%c3%b3n/BC-189483
     ```

## Usage

### Running the Tests
1. **Run All Tests**
   Execute the script to run all test cases:
   ```bash
   python test_automation.py
   ```

2. **Individual Tests**
   Run individual test functions as needed by modifying the `test_automation.py` file.

### Report Generation
- Test results are saved in the `reports` directory.
- The file is named `test_report.xlsx` and contains columns for `testcase`, `result`, and `comments`.

### Test Cases
#### 1. **H1 Tag Existence**
   - Validates the existence of an H1 tag on the page.
   - Pass/Fail status with appropriate comments.

#### 2. **HTML Tag Sequence Test**
   - Checks for missing or improperly ordered HTML tags (H1 to H6).

#### 3. **Image Alt Attribute Test**
   - Ensures all images on the page have a valid `alt` attribute.

#### 4. **URL Status Code Test**
   - Verifies that all URLs on the page are functional (not returning a 404 error).

#### 5. **Currency Filter Test**
   - Selects each currency from the dropdown menu and validates that property tiles display the correct currency symbol.

#### 6. **Script Data Extraction**
   - Extracts data from the JavaScript `ScriptData` object, such as SiteURL, CampaignID, SiteName, and more.

## Structure
```
project-directory/
├── utils.py                 # Contains utility functions like save_report and driver_setup
├── test_h1_tag_existence.py # Test for H1 tag existence
├── test_html_sequence.py    # Test for HTML tag sequence
├── test_image_alt.py        # Test for image alt attributes
├── test_url_status.py       # Test for URL status codes
├── test_currency_filter.py  # Test for currency filter functionality
├── test_script_data.py      # Test for script data extraction
├── requirements.txt         # Python dependencies
├── reports/                 # Directory for reports
├── .env                     # Environment variables
├── chromedriver             # Chrome WebDriver executable
└── README.md                # Project documentation
```

## Additional Notes
- **Logging**: The script uses Python's `logging` module to log test progress and errors.
- **Browser Window**: The script launches Chrome in full-screen mode for better visibility and accuracy.
- **Scalability**: The modular structure allows easy addition of new test cases.


**Happy Testing!**

