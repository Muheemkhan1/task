from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Replace these with your actual credentials
username = "L1group@utopusinsights.com"
password = "Utopus@2021"

# Specify the path to the Chrome driver executable
chrome_driver_path = r'C:\Users\MuheemKhan\Downloads\chromedriver_win32\chromedriver.exe'

# Initialize Chrome options and set the executable path
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"webdriver.chrome.driver={'C:\\Users\MuheemKhan\Downloads\chromedriver_win32\chromedriver.exe'}")

# Initialize the web driver with the Chrome options
driver = webdriver.Chrome(chrome_options=chrome_options)

# Open the login page
driver.get("https://scipher.fx.utopusinsights.io/login")  # Replace with the URL of your login page

# Find the username and password input fields and submit button
username_input = driver.find_element(By.ID, "Username")  # Replace with the actual element's ID
password_input = driver.find_element(By.ID, "Password")  # Replace with the actual element's ID
login_button = driver.find_element(By.ID, "signInSubmitButton")  # Replace with the actual element's ID

# Enter your credentials and click the login button
username_input.send_keys(username)
password_input.send_keys(password)
login_button.click()

# Wait for the login to complete (you may need to adjust the time)
time.sleep(5)

# Navigate to the monitoring page
driver.get("https://scipher.fx.utopusinsights.io/forecast/farm-forecast?asset_id=389861",
    "https://scipher.fx.utopusinsights.io/forecast/farm-forecast?asset_id=594239")  # Replace with the URL of the monitoring page

# Take a snippet of the first farm's monitoring section
farm1_element = driver.find_element(By.ID, "farm1_section_id")  # Replace with the actual element's ID
farm1_screenshot = farm1_element.screenshot_as_png
with open("farm1_screenshot.png", "wb") as file:
    file.write(farm1_screenshot)

# Take a snippet of the second farm's monitoring section
farm2_element = driver.find_element(By.ID, "farm2_section_id")  # Replace with the actual element's ID
farm2_screenshot = farm2_element.screenshot_as_png
with open("farm2_screenshot.png", "wb") as file:
    file.write(farm2_screenshot)

# Close the browser
driver.quit()


