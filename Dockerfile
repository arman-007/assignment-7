# Use an official Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies for Selenium
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    firefox-esr \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Install GeckoDriver
RUN wget -q "https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz" \
    -O /tmp/geckodriver.tar.gz && \
    tar -xzf /tmp/geckodriver.tar.gz -C /usr/local/bin && \
    rm /tmp/geckodriver.tar.gz && \
    chmod +x /usr/local/bin/geckodriver

# Install ChromeDriver and Google Chrome
RUN wget -q "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" -O /tmp/chrome.deb && \
    apt-get update && apt-get install -y /tmp/chrome.deb && rm /tmp/chrome.deb && \
    wget -q "https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.87/linux64/chromedriver-linux64.zip" \
    -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /tmp && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose a default port (optional, if using Flask/Django for the project)
EXPOSE 5000

# Default command to run the test
# CMD ["python", "test_automation.py"]
