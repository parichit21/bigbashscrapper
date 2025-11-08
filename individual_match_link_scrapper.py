import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

# Path to the ChromeDriver executable
chrome_driver_path = r'C:\Users\91965\Desktop\cricketdatascience\chromedriver-win64\chromedriver-win64\chromedriver.exe'

# XPath for the target element
element_xpath = "//a[contains(@class, 'ds-no-tap-higlight')]"

try:
    # Set up the WebDriver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # URL to scrape
    url = "https://www.espncricinfo.com/series/big-bash-league-2020-21-1226769/match-schedule-fixtures-and-results"  # Replace with the actual URL
    driver.get(url)

    # Find elements using XPath
    elements = driver.find_elements(By.XPATH, element_xpath)

    # Extract href attribute from elements
    data = [element.get_attribute("href") for element in elements]

    # Save data to a CSV file
    csv_file_path = 'output.csv'
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Href Value"])  # Header row
        for row in data:
            writer.writerow([row])

    print(f"Data saved to {csv_file_path}")

except WebDriverException as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    if 'driver' in locals():
        driver.quit()