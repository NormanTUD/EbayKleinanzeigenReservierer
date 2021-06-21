from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException        
from selenium.webdriver.common.keys import Keys

import time
import os
from pprint import pprint

import easygui
import os.path
from simplebeep import beep
import argparse
import pathlib

import random
import string


parser = argparse.ArgumentParser(description='Auto-reserve eBay Kleinanzeigen')

parser.add_argument('--username', type=str, help='Username')
parser.add_argument('--password', type=str, help='Password')

args = parser.parse_args()

username = args.username
password = args.password

basepath = pathlib.Path(__file__).parent.absolute()
path = None

if os.name == 'nt':
    path = str(basepath) + "/chromedriver.exe"
    if not os.path.isfile(path) :
        wd = sys._MEIPASS
        path = os.path.join(wd, "chromedriver.exe")
elif os.name == "posix":
    path = str(basepath) + "/chromedriver"

login_url = "https://www.ebay-kleinanzeigen.de/m-einloggen.html?targetUrl=/";

options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(executable_path=path, options=options)
driver.get(login_url)

timeout = 30

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def speak (text):
    os.system("pico2wave -l=de-DE -w=/tmp/notice.wav '" + text + "'; aplay /tmp/notice.wav; rm /tmp/notice.wav")

def get_element(locator):
    item = WebDriverWait(driver, timeout).until(expected_conditions.presence_of_element_located(locator))
    return item

def accept_cookies ():
    try:
        accept_cookies_button = get_element((By.ID, "gdpr-banner-accept"))
        accept_cookies_button.click()
    except Exception as e:
        print(e)

def login ():
    username_input = get_element((By.ID, "login-email"))
    password_input = get_element((By.ID, "login-password"))
    submit = get_element((By.ID, "login-submit"))

    username_input.send_keys(username)
    time.sleep(2)
    password_input.send_keys(password)
    submit.click()

def search (term):
    driver.find_element_by_id('site-search-query').send_keys(Keys.CONTROL + "a")
    driver.find_element_by_id('site-search-query').send_keys(Keys.DELETE)
    search_field = get_element((By.ID, "site-search-query"))
    submit = get_element((By.ID, "site-search-submit"))
    search_field.send_keys(term)
    submit.click()

def go_through_search_results ():
    elements = driver.find_elements_by_class_name('aditem')
    for element in elements:
        href = element.get_attribute('data-href')
        adid = element.get_attribute('data-adid')
        print(href)

def goto_startpage():
    driver.get("https://ebay-kleinanzeigen.de")

accept_cookies()
login()
search("runkelrübenverbot")
search("computer")
go_through_search_results()
goto_startpage();
