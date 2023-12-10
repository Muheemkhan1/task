from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Replace the following with your own credentials
username = "L1group@utopusinsights.com"
password = "Utopus@2021"

# Replace the following with the URL of the website you want to log in to
url = "https://scipher.fx.utopusinsights.io/login"

# Create a new Chrome browser instance (assuming Chrome WebDriver is in the system PATH)
driver = webdriver.Chrome()

# Navigate to the login page
driver.get(url)

# Find the username and password fields and enter your credentials
driver.find_element_by_xpath("//input[@id='signInFormUsername']")  # Assuming the input field name is "username"
username_field.send_keys(username)
driver.find_element_by_xpath("//input[@name='password']")  # Assuming the input field name is "password"
password_field.send_keys(password)

# Submit the login form
password_field.send_keys(Keys.RETURN)

# Explicitly wait for the login page to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dashboard-header")))

# Define the URLs to capture screenshots of
urls = [
    "https://scipher.fx.utopusinsights.io/forecast/farm-forecast?asset_id=389861",
    "https://scipher.fx.utopusinsights.io/forecast/farm-forecast?asset_id=594239"
]

# Loop through the URLs and capture a screenshot of each page
for i, url in enumerate(urls):
    driver.get(url)
    filename = f"screenshot_{i+1}.png"  # Customize the filename pattern if needed
    driver.save_screenshot(filename)
    print(f"Screenshot saved to {filename}")

# Close the browser after capturing all screenshots
driver.quit()
