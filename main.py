from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

# Set up WebDriver (Make sure you have ChromeDriver installed)

print("-- Setting chrome options --")
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
chrome_options.add_argument("--disable-gpu")  # Prevent potential GPU-related issues
chrome_options.add_argument("--window-size=1920x1080")  # Set a virtual window size
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model (useful for Linux servers)
chrome_options.add_argument("--disable-dev-shm-usage")  # Prevent shared memory issues in containers

driver = webdriver.Chrome(options=chrome_options)

# Step 1: Open the login page
print("-- Opening page --")

login_url = "https://copiesenligne.cned.fr/Accueil.aspx"
driver.get(login_url)

# Wait for redirection to login page
time.sleep(1)  # Adjust if necessary

# Step 2: Enter login credentials
creds = "creds.txt"  # Path to credentials file

if os.path.exists(creds):
    with open(creds, "r") as file:
        lines = file.readlines()

        creds1 = lines[0].strip() if len(lines) > 0 else ""
        creds2 = lines[1].strip() if len(lines) > 1 else ""

else:
    creds1, creds2 = "", ""

username = creds1
password = creds2

# Find the username field and enter the username
username_field = driver.find_element(By.NAME, "UserName")  # Adjust if needed
username_field.send_keys(username)

# Find the password field and enter the password
password_field = driver.find_element(By.NAME, "Password")  # Adjust if needed
password_field.send_keys(password)

# Submit the login form
print("-- Logging in --")

password_field.send_keys(Keys.RETURN)

# Step 3: Wait for the redirection to the main page
time.sleep(2)  # Adjust if needed

# Step 4: Scrape the data from the span
file_path = "data.txt"

try:
    # Scraping the data
    print("-- Getting data --")

    given = driver.find_element(By.ID, "ContentPlaceHolderMenu_LabelNombreCopiesDeposees").text
    correcting = driver.find_element(By.ID, "ContentPlaceHolderMenu_LabelNombreCorrectionsEnCours").text
    corrected = driver.find_element(By.ID, "ContentPlaceHolderMenu_LabelNombreCopiesCorrigees").text

    new_data = f"{given},{correcting},{corrected}"

    # Check if the file exists
    if os.path.exists(file_path):
        # Read the previous data
        with open(file_path, "r") as file:
            old_data = file.read().strip()

        # Compare with new data
        if new_data == old_data:
            print("Data haven't changed !")
        else:
            print(f"New Data:\nGiven homeworks: {given}\nIn correction: {correcting}\nCorrected: {corrected}")
            # Update the file
            with open(file_path, "w") as file:
                file.write(new_data)
    else:
        # File does not exist, create it and save initial data
        with open(file_path, "w") as file:
            file.write(new_data)
        print(f"File created with initial data:\nGiven homeworks: {given}\nIn correction: {correcting}\nCorrected: {corrected}")

except Exception as e:
    print("An error occurred:", e)


# Close the browser
driver.quit()
