import time
import random
import os
import sqlite3
import sys
import platform
from imap_tools import MailBox, AND
from bs4 import BeautifulSoup
from selenium import webdriver
from dotenv import load_dotenv, find_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import date


def get_email():
    load_dotenv(find_dotenv())
    user = os.environ.get("email_login")
    password_email = os.environ.get("email_password")
    server = "imap.gmail.com"
    mb = MailBox(server).login(user, password_email)
    messages = mb.fetch(criteria=AND(seen=False, from_="luckynano.com"),
                        mark_seen=True,
                        bulk=True)
    for msg in messages:
        soup = BeautifulSoup(msg.html, 'html.parser')
        el = soup.find(href=True)
        url = el['href']
        return url


def get_login_and_password():
    login = os.environ.get("nano_login")
    password = os.environ.get("nano_password")
    return login, password


def initialize_db():
    conn = sqlite3.connect('nano_amount.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS nano_amount (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nano TEXT,
    date_added DATE)
''')
    conn.commit()
    conn.close()

def check_if_link_exist(nano_amount, current_date):
    conn = sqlite3.connect('nano_amount.db')
    c = conn.cursor()
    c.execute("INSERT INTO nano_amount (nano, date_added) VALUES (?, ?)", (nano_amount, current_date))
    conn.commit()
    conn.close()

def make_withdraw():
    driver.find_element(By.CSS_SELECTOR, "#header_content > div.account_name").click()
    time.sleep(random.randint(2, 4))
    driver.find_element(By.CSS_SELECTOR, "#withdraw_button").click()
    time.sleep(random.randint(2, 4))
    driver.find_element(By.CSS_SELECTOR, "#withdraw_button_max").click()
    time.sleep(random.randint(2, 4))
    driver.find_element(By.CSS_SELECTOR, "#withdraw_button_ok").click()
    time.sleep(1)
    text_error_message = check_error()
    if text_error_message[:6] == "Please":
        driver.close()
        sys.exit()


def check_error():
    error_window = driver.find_element(By.CSS_SELECTOR, "#error_window")
    if error_window:
        return error_window.text


load_dotenv(find_dotenv())
prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
chrome_options = Options()
chrome_options.add_argument('start-maximized')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
login, password = get_login_and_password()
if platform.system() == "Linux":
    driver = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_options)
else:
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=chrome_options)
driver.get("https://www.luckynano.com/")
driver.maximize_window()
driver.implicitly_wait(10)
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "#ihm_login_button > span").click()
time.sleep(random.randint(1, 3))
driver.find_element(By.CSS_SELECTOR, "#name").send_keys(login)
time.sleep(random.randint(1, 3))
driver.find_element(By.CSS_SELECTOR, "#pw").send_keys(password)
time.sleep(random.randint(1, 3))
driver.find_element(By.CSS_SELECTOR, "#login_form_button > span").click()
time.sleep(random.randint(2, 4))
nano_amount = driver.find_element(By.CSS_SELECTOR, "#header_nano_count > span").text
make_withdraw()
url = get_email()
while not url:
    time.sleep(10)
    url = get_email()
driver.get(url)
time.sleep(2)
driver.close()
current_date = date.today()
initialize_db()
check_if_link_exist(nano_amount, current_date)
