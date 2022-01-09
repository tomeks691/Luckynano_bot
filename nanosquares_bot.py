import time
import json
import random
import telegram_send
import platform
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


def send_notification(message):
    telegram_send.send(messages=[f"{message}"])


def get_lottery_time():
    chat = driver.find_element_by_css_selector("#chat-input")
    chat.send_keys("/lottery")
    chat.send_keys(Keys.RETURN)
    lottery_time = driver.find_elements_by_class_name("chat_system_message")
    send_notification(lottery_time[-1].text)
    if lottery_time[-1].text[-8:] == "a prize.":
        chat = driver.find_element_by_css_selector("#chat-input")
        chat.send_keys("lotto")
        time.sleep(1)
        chat.send_keys(Keys.RETURN)
    else:
        print(lottery_time[-1].text[-8:])


def play_minigame():
    the_end = True
    coins = int(driver.find_element_by_css_selector("#header_silver_count").text)
    if coins >= 60:
        while coins > 0:
            time.sleep(1)
            driver.find_element_by_css_selector(
                "#header_content > div.header_game_wrapper > div.header_game.mini_dice"
            ).click()
            time.sleep(random.randint(2, 3))
            driver.find_element_by_css_selector("#dice_bet_auto").click()
            time.sleep(random.randint(2, 3))
            driver.find_element_by_css_selector("#dice_auto_bet > input[type=number]").send_keys(f"{Keys.BACKSPACE}4")
            time.sleep(random.randint(2, 3))
            driver.find_element_by_css_selector("#dice_auto_start").click()
            while coins > 0:
                time.sleep(random.randint(1, 20))
                coins = int(driver.find_element_by_css_selector("#header_silver_count").text)


def faucet_coin():
    driver.find_element_by_css_selector("#ihm_faucet_button").click()
    time.sleep(random.randint(1, 2))
    driver.find_element_by_css_selector("#bonus_claim").click()


def waiting_and_ending_driver():
    driver.close()
    time.sleep(random.randint(1800, 1810))


def get_login_and_password():
    with open("login_and_password.json", "r") as f:
        data = json.load(f)
    login, password = data.values()
    return login, password


prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
chrome_options = Options()
chrome_options.add_argument("--lang=pl")
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option(
    "prefs", {"profile.managed_default_content_settings.javascript": 1}
)
chrome_options.add_experimental_option("useAutomationExtension", False)
login, password = get_login_and_password()
while True:
    try:
        if platform.system() == "Linux":
            driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', chrome_options=chrome_options)
        elif platform.system() == "Windows":
            driver = webdriver.Chrome(
                ChromeDriverManager().install(), chrome_options=chrome_options
            )
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if current_time == "22:30:50":
            time.sleep(300)
        driver.get("https://www.luckynano.com/")
        driver.maximize_window()
        driver.implicitly_wait(10)
        time.sleep(1)
        driver.find_element_by_css_selector("#ihm_login_button > span").click()
        time.sleep(random.randint(1, 3))
        driver.find_element_by_css_selector("#name").send_keys(login)
        time.sleep(random.randint(1, 3))
        driver.find_element_by_css_selector("#pw").send_keys(password)
        time.sleep(random.randint(1, 3))
        driver.find_element_by_css_selector("#login_form_button > span").click()
        send_notification("Logowanie poprawne!")
        time.sleep(random.randint(2, 4))
        get_lottery_time()
        time.sleep(random.randint(2, 4))
        faucet_coin()
        time.sleep(random.randint(2, 4))
        play_minigame()
        time.sleep(1)
        send_notification("Koniec")
        waiting_and_ending_driver()
    except:
        driver.close()
        continue
