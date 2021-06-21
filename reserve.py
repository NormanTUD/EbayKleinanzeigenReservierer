from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException        
from selenium.webdriver.common.keys import Keys
import urllib.request
import re

import sys
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
parser.add_argument('--ekz_watcher_url', type=str, help='EKZ-Watcher-URL')
parser.add_argument('--ekz_watcher_pw', type=str, help='EKZ-Watcher password')

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
        if already_written_to(adid) == 0:
            print("WRITE TO " + adid);

def goto_startpage():
    driver.get("https://ebay-kleinanzeigen.de")

def already_written_to (anzeige_id):
    with urllib.request.urlopen(args.ekz_watcher_url + "?pw=" + args.ekz_watcher_pw) as f:
        html = f.read().decode('utf-8')
        regex = "<tr><td>" + str(anzeige_id) + "</td>"
        if regex in html:
            return 1
    return 0

def add_to_ekz_watcher (anzeige_id, link, reservierung_id):
    url = args.ekz_watcher_url + "?pw=" + args.ekz_watcher_pw + "&anzeige_id=" + str(anzeige_id) + "&link=" + link + "&reservierung_id=" + str(reservierung_id)
    return url

#print(already_written_to("123"));
#print(add_to_ekz_watcher(123, "asdf", 12345))
#sys.exit()


login_url = "https://www.ebay-kleinanzeigen.de/m-einloggen.html?targetUrl=/";

options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(executable_path=path, options=options)
driver.get(login_url)

accept_cookies()
login()
search("runkelrübenverbot")
go_through_search_results()
goto_startpage();
