from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException        
from selenium.webdriver.common.keys import Keys
import urllib.request
import re

import typo
from random import randrange

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

parser.add_argument('--username', type=str, help='Username', required=True)
parser.add_argument('--password', type=str, help='Password', required=True)
parser.add_argument('--ekz_watcher_url', type=str, help='EKZ-Watcher-URL', required=True)
parser.add_argument('--ekz_watcher_pw', type=str, help='EKZ-Watcher password', required=True)
parser.add_argument('--keyword', action="append", type=str, help='Keywords (can be used multiple times)')
parser.add_argument('--typos', action="store_true", help='Search for typos')
parser.add_argument('--sleep_random', action="store_true", help='Sleep for a random time after searching')

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
            go_to_and_write_to_anzeige(href, adid)

def go_to_and_write_to_anzeige (href, adid):
    url = "https://ebay-kleinanzeigen.de/" + href
    driver.get(url)
    reservierung_id = get_random_string(10)

    reservierung_text = "Hallo, ich habe voraussichtlich Interesse an dem Artikel / den Artikeln. Daher möchte ich um eine Reservierung für 24 Stunden bitten. Sollte ich mich bis dahin nicht nochmals gemeldet haben, verfällt die Reservierung meinerseits automatisch. Da ich nicht allein darüber entscheiden kann, könnte es auch sein, dass sich mein Kollege meldet. Dieser gibt dann den folgenden Reservierungscode zur Verifikation durch:\n\nReservierungscode: " + reservierung_id + "\n\nVielen Dank"

    contact_text = get_element((By.CLASS_NAME, "viewad-contact-message"))
    contact_text.send_keys(reservierung_text)
    contact_text.submit()

    add_to_ekz_watcher(adid, href, reservierung_id)

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
    with urllib.request.urlopen(url) as f:
        html = f.read().decode('utf-8')

def get_typo_string(myStrError):
    myrand = randrange(12)
    myStrErrer = myStrError

    if myrand == 0:
        myStrErrer = typo.StrErrer(myStrError).char_swap()
    elif myrand == 1:
        myStrErrer = typo.StrErrer(myStrError).missing_char()
    elif myrand == 2:
        myStrErrer = typo.StrErrer(myStrError).missing_char()
    elif myrand == 3:
        myStrErrer = typo.StrErrer(myStrError).extra_char()
    elif myrand == 4:
        myStrErrer = typo.StrErrer(myStrError).nearby_char()
    elif myrand == 5:
        myStrErrer = typo.StrErrer(myStrError).similar_char()
    elif myrand == 6:
        myStrErrer = typo.StrErrer(myStrError).skipped_space()
    elif myrand == 7:
        myStrErrer = typo.StrErrer(myStrError).random_space()
    elif myrand == 8:
        myStrErrer = typo.StrErrer(myStrError).repeated_char()
    elif myrand == 9:
        myStrErrer = typo.StrErrer(myStrError).unichar()
    elif myrand == 10:
        myStrErrer = typo.StrErrer(myStrError).unichar().char_swap()
    elif myrand == 11:
        myStrErrer = typo.StrErrer(myStrError).char_swap().missing_char()
    elif myrand == 12:
        myStrErrer = typo.StrErrer(myStrError).char_swap().missing_char()

    return str(myStrErrer)

login_url = "https://www.ebay-kleinanzeigen.de/m-einloggen.html?targetUrl=/";

options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(executable_path=path, options=options)
driver.get(login_url)

accept_cookies()
login()
while True:
    for item in args.keyword:
        search(item)
        go_through_search_results()
        if args.typos:
            search(get_typo_string(item))
            go_through_search_results()
        if args.sleep_random:
            sleeptime = randrange(30)
            time.sleep(sleeptime)
