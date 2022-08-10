import os
import platform
import random
import time
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager


def get_lottery_time():
    chat = driver.find_element(By.CSS_SELECTOR, "#chat-input")
    chat.send_keys("/lottery")
    chat.send_keys(Keys.RETURN)
    lottery_time = driver.find_elements(By.CLASS_NAME, "chat_system_message")
    if lottery_time[-1].text[-8:] == "a prize.":
        chat = driver.find_element(By.CSS_SELECTOR, "#chat-input")
        chat.send_keys("lotto")
        time.sleep(1)
        chat.send_keys(Keys.RETURN)
    else:
        print(lottery_time[-1].text[-8:])


def play_minigame():
    coins = int(driver.find_element(By.CSS_SELECTOR, "#header_silver_count").text)

    if coins >= 60:
        while coins > 0:
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR,
                                "#header_content > div.header_game_wrapper > div.header_game.mini_dice").click()
            time.sleep(random.randint(2, 3))
            driver.find_element(By.CSS_SELECTOR, "#dice_bet_auto").click()
            time.sleep(random.randint(2, 3))
            driver.find_element(By.CSS_SELECTOR, "#dice_auto_bet > input[type=number]").send_keys(f"{Keys.BACKSPACE}4")
            time.sleep(random.randint(2, 3))
            driver.find_element(By.CSS_SELECTOR, "#dice_auto_start").click()
            while coins > 0:
                time.sleep(random.randint(1, 20))
                coins = int(driver.find_element(By.CSS_SELECTOR, "#header_silver_count").text)


def faucet_coin():
    driver.find_element(By.CSS_SELECTOR, "#ihm_faucet_button").click()
    time.sleep(random.randint(1, 2))
    driver.find_element(By.CSS_SELECTOR, "#bonus_claim").click()


def get_login_and_password():
    login = os.environ.get("nano_login")
    password = os.environ.get("nano_password")
    return login, password


load_dotenv(find_dotenv())
prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
firefox_options = Options()
firefox_options.add_argument('start-maximized')
firefox_options.add_argument('--headless')
firefox_options.add_argument('--no-sandbox')
firefox_options.add_argument('--disable-dev-shm-usage')
login, password = get_login_and_password()
print(login, password)

# if platform.system() == "Linux":
#     driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=firefox_options)
# else:
s = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=s, options=firefox_options)
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
if current_time == "22:30:50":
    time.sleep(300)
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
get_lottery_time()
time.sleep(random.randint(2, 4))
faucet_coin()
time.sleep(random.randint(2, 4))
play_minigame()
time.sleep(1)
driver.close()
