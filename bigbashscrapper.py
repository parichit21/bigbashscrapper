import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from lxml import html

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

# Path to the ChromeDriver executable
chrome_driver_path = r'C:\Users\91965\Desktop\cricketdatascience\chromedriver-win64\chromedriver-win64\chromedriver.exe'
Toss_Xpath = "//td[@class='ds-text-typo']/span[@class='ds-text-tight-s ds-font-regular']"
city_venue_xpath ="//a[@class='ds-inline-flex ds-items-start ds-leading-none']/span[@class='ds-text-tight-s ds-font-medium ds-block ds-text-typo ds-underline ds-decoration-ui-stroke hover:ds-text-typo-primary hover:ds-decoration-ui-stroke-primary']"

# Input and output CSV file paths
input_csv_path = 'output.csv'  # Replace with the path to your input CSV file
output_csv_path = 'toss_details.csv'

try:
    # Set up the WebDriver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Read URLs from the input CSV file
    with open(input_csv_path, mode='r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        urls = [row[0] for idx, row in enumerate(reader) if idx > 0]  # Skip the header row

    # Prepare to write toss details to the output CSV file
    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["URL", "Toss Winner", "Elected"])  # Write header row

        # Process each URL
        for url in urls:
            try:
                # Navigate to the URL
                driver.get(url)

                # Extract the HTML content
                html_content = driver.page_source

                # Check if the page source is empty
                if not html_content.strip():
                    writer.writerow([url, "Error: Empty document", ""])
                    continue

                # Parse the HTML content
                tree = html.fromstring(html_content)
                toss_details = tree.xpath(Toss_Xpath)

                # Process toss details
                if toss_details:
                    toss_text = toss_details[0].text_content()
                    if ',' in toss_text:
                        toss_winner, elected_action = toss_text.split(',', 1)
                        toss_winner = toss_winner.strip()
                        elected_action = "bat" if "bat" in elected_action.lower() else "field"
                        writer.writerow([url, toss_winner, elected_action])
                    else:
                        writer.writerow([url, "Invalid toss details", ""])
                else:
                    writer.writerow([url, "No toss details found", ""])

            except WebDriverException as e:
                writer.writerow([url, f"Error: {e}", ""])

    print(f"Toss details saved to {output_csv_path}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    if 'driver' in locals():
        driver.quit()