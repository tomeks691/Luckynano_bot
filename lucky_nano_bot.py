import os
import platform
import random
import time
import psutil
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def kill_pid():
    proc_name = "chromium-browser"
    for proc in psutil.process_iter():
        if proc.name() == proc_name:
            proc.kill()


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
            time.sleep(random.randint(3, 5))
            driver.find_element(By.CSS_SELECTOR, "#dice_bet_auto").click()
            time.sleep(random.randint(3, 5))
            driver.find_element(By.CSS_SELECTOR, "#dice_auto_bet > input[type=number]").send_keys(f"{Keys.BACKSPACE}4")
            time.sleep(random.randint(3, 5))
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
if platform.system() == "Linux":
    kill_pid()