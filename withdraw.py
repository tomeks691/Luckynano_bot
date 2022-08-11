import time
import random
import os
from imap_tools import MailBox, AND
from bs4 import BeautifulSoup
from selenium import webdriver
from dotenv import load_dotenv, find_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import telepot
import platform


def get_email():
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


def make_withdraw():
    driver.find_element_by_css_selector("#header_content > div.account_name").click()
    time.sleep(random.randint(2, 4))
    driver.find_element_by_css_selector("#withdraw_button").click()
    time.sleep(random.randint(2, 4))
    driver.find_element_by_css_selector("#withdraw_button_max").click()
    time.sleep(random.randint(2, 4))
    driver.find_element_by_css_selector("#withdraw_button_ok").click()

load_dotenv(find_dotenv())
prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
chrome_options = Options()
chrome_options.add_argument("--lang=pl")
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option(
    "prefs", {"profile.managed_default_content_settings.javascript": 1}
)
chrome_options.add_experimental_option("useAutomationExtension", False)
login, password = get_login_and_password()
if platform.system() == "Linux":
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', chrome_options=chrome_options)
elif platform.system() == "Windows":
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(
        service=s, chrome_options=chrome_options
    )
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
time.sleep(50)
url = get_email()
driver.get(url)
time.sleep(10)
driver.close()
