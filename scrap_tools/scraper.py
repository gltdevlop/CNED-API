from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import requests

# URL to which you want to send the GET


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
    

def scrape_data_ns(creds):
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


        driver.quit()

        return {
                "data": {
                    "given_homeworks": given,
                    "in_correction": correcting,
                    "corrected": corrected
                }
            }
    except Exception as e:
        driver.quit()
        return {"error": str(e)}


def checking():
    url = 'http://127.0.0.1:5000/hws'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        new = data['new_data']
        old = data['old_data']

        # Convert values to integers for comparison
        corrected_diff = int(new['corrected']) - int(old['corrected'])
        in_correction_diff = int(new['in_correction']) - int(old['in_correction'])

        # Only show the message if there's a change
        if corrected_diff is not None or in_correction_diff is not None:
            return f"{in_correction_diff} devoir(s) passé(s) en correction, {corrected_diff} nouveau(x) devoir(s) corrigé(s) !"

def checking_cor():
    url = 'http://127.0.0.1:5000/hws'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        new = data['new_data']
        old = data['old_data']

        # Convert values to integers for comparison
        corrected_diff = int(new['corrected']) - int(old['corrected'])

        # Only show the message if there's a change
        if corrected_diff is not None:
            return f"{corrected_diff} nouveau(x) devoir(s) corrigé(s) !"


def checking_incor():
    url = 'http://127.0.0.1:5000/hws'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        new = data['new_data']
        old = data['old_data']

        # Convert values to integers for comparison
        in_correction_diff = int(new['in_correction']) - int(old['in_correction'])

        # Only show the message if there's a change
        if in_correction_diff is not None:
            return f"{in_correction_diff} devoir(s) passé(s) en correction !"