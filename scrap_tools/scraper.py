from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

def scrape_data(creds, data):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    login_url = "https://copiesenligne.cned.fr/Accueil.aspx"
    driver.get(login_url)
    time.sleep(1)

    creds = creds

    if os.path.exists(creds):
        with open(creds, "r") as file:
            lines = file.readlines()
            creds1 = lines[0].strip() if len(lines) > 0 else ""
            creds2 = lines[1].strip() if len(lines) > 1 else ""
    else:
        return {"error": "Credentials file not found"}

    try:
        username_field = driver.find_element(By.NAME, "UserName")
        username_field.send_keys(creds1)

        password_field = driver.find_element(By.NAME, "Password")
        password_field.send_keys(creds2)

        password_field.send_keys(Keys.RETURN)

        time.sleep(2)

        given = driver.find_element(By.ID, "ContentPlaceHolderMenu_LabelNombreCopiesDeposees").text
        correcting = driver.find_element(By.ID, "ContentPlaceHolderMenu_LabelNombreCorrectionsEnCours").text
        corrected = driver.find_element(By.ID, "ContentPlaceHolderMenu_LabelNombreCopiesCorrigees").text

        data_path = data
        new_data = f"{given},{correcting},{corrected}"

        old_given, old_correcting, old_corrected = "", "", ""

        if os.path.exists(data_path):
            with open(data_path, "r") as file:
                old_data = file.read().strip().split(",")
            old_given = old_data[0] if len(old_data) > 0 else ""
            old_correcting = old_data[1] if len(old_data) > 1 else ""
            old_corrected = old_data[2] if len(old_data) > 2 else ""

            with open(data_path, "w") as file:
                file.write(new_data)
        else:
            with open(data_path, "w") as file:
                file.write(new_data)

        driver.quit()

        if not os.path.exists(data_path):
            return {
                "old_data": {
                    "given_homeworks": "None",
                    "in_correction": "None",
                    "corrected": "None"
                },
                "new_data": {
                    "given_homeworks": given,
                    "in_correction": correcting,
                    "corrected": corrected
                }
            }
        else:
            return {
                "old_data": {
                     "given_homeworks": old_given,
                    "in_correction": old_correcting,
                    "corrected": old_corrected
                },
                "new_data": {
                    "given_homeworks": given,
                    "in_correction": correcting,
                    "corrected": corrected
                }
            }



    except Exception as e:
        driver.quit()
        return {"error": str(e)}
