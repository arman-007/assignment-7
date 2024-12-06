### Downloading setting up ChromeDriver:

#### 1. Go to the ChromeDriver Download page.
- Download the Chrome Driver with the same version as your updated Chrome.
- Click the link on the Chrome for Testing availability dashboard: https://chromedriver.chromium.org/downloads
- https://googlechromelabs.github.io/chrome-for-testing/ to find the Chrome Driver matching your updated Chrome version.
  
#### 2. Download the ChromeDriver.
- Download the Chrome Driver version that matches your Chrome.
- https://googlechromelabs.github.io/chrome-for-testing/
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