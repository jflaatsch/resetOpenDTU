#! Python 3.12
# reset OpenDTU
#
# by Jonathan Laatsch
# 25 Feb 2025

import time
import sys, os
import datetime as dt
#import keyring
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.common.action_chains import ActionChains
#from pyvirtualdisplay import Display

DEBUG = False #NOTE: DEBUG = True disables reboot confirmation step for testing
WATCH_BROWSER = False
DT_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
URL = f'http://192.168.189.3/maintenance/reboot'
SERVICE_NAME = 'OpenDTU'
USERNAME = 'OPENDTU_USER'
PASSWORD = 'OPENDTU_PASS'
REATTEMPT_LIMIT = 3
CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
FIREFOX_BINARY_PATH = r'/usr/bin/firefox-esr'
GECKODRIVER_PATH = '/usr/bin/geckodriver'

def wait_and_click(wait, driver, type, element):
    """
    :param wait: WebDriverWait object
    :param type: By.type...
        - 'id' = By.ID
        - 'xpath' = By.XPATH
    :param element: search string to apply to (By.type, element)
    :return: None
    """

    if type.lower() == 'id':
        element = wait.until(EC.element_to_be_clickable((By.ID, element)))
    elif type.lower() == 'xpath':
        element = wait.until(EC.element_to_be_clickable((By.XPATH, element)))
    driver.execute_script('return arguments[0].scrollIntoView(true);', element)
    element.click()
    if DEBUG: 
        time.sleep(3)
        print(driver.title, driver.current_url)
    return None


def wait_login(wait, driver):
    try:
        username_element = wait.until(EC.element_to_be_clickable((By.NAME, "username")))
        username_element.clear()
#        username = keyring.get_password(SERVICE_NAME, 'username')
        username = os.environ.get(USERNAME) #TODO: replace this with working keyring
        username_element.send_keys(username) 
        username = None

        password_element = wait.until(EC.element_to_be_clickable((By.NAME, "password")))
        password_element.clear()
#        password = keyring.get_password(SERVICE_NAME, 'password')
        password = os.environ.get(PASSWORD) #TODO: replace this with working keyring
        password_element.send_keys(password)
        password = None

        password_element.send_keys(Keys.RETURN) #submit form
        return True

    except exceptions.ElementClickInterceptedException:
        print('login button not found...')
        return False
    except exceptions.TimeoutException:
        print('login did not appear...')
        return False


def wait_reboot(wait, driver):
    try:
        element = '//button[text()="Reboot!"]' #reboot button (first)
        wait_and_click(wait, driver, 'xpath', element)
        element = '//button[@type="button" and text()="Reboot!"]' #confirmation button
        if not DEBUG: 
            wait_and_click(wait, driver, 'xpath', element)
            print('Wait for OpenDTU restart...')
        else:
            #TODO: this should select the Reboot! confirmation button for the user
            # element = wait.until(EC.element_to_be_clickable((By.XPATH, element)))
            # actions = ActionChains(driver)
            # actions.move_to_element(element).perform() #TODO: fix this syntax
            # print(f'Press enter to activate the reboot.')
            if WATCH_BROWSER: 
                print('Click Reboot! confirmation if desired...')
                time.sleep(10) #ten seconds to click Reboot! button manually
            elif DEBUG:
                print(f'Click Reboot! confirmation is not automated in DEBUG mode.')
                # following will cause an error in crontab implementation
                #do_click = input('yes, to reboot, NO otherwise: ')
                #if do_click.lower() == 'yes':
                #   wait_and_click(wait, driver, 'xpath', element)
                #   print('Wait for OpenDTU restart...')
        return True
    except exceptions.ElementClickInterceptedException:
        print('reset covered by another frame?...')
        return False
    except exceptions.TimeoutException:
        print(f'did not find {element}...')
        return False


def click_reset(url):
    """
        Parameters:
            - url - source page to capture
        Return:
            - success - boolean reporting
    """
#    with Display(visible= WATCH_BROWSER, size=(960, 540)):
        #display.start()

    # initiate the webdriver:
    #TODO: optionally could make this work with FireFox too
    #if DEBUG: print('loading Firefox options...')
    #options = webdriver.FirefoxOptions()
    #options.binary_location = CHROMEDRIVER_PATH
    #options.add_argument('--headless')
    #service = Service(GECKODRIVER_PATH)
    #driver = webdriver.Firefox(options=options, service=service) #requires geckodriver installed
    # originally used Chrome driver
    if DEBUG: print('loading Chrome options...')
    service = Service(executable_path=CHROMEDRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    if DEBUG: print('initializing webdriver...')
    driver = webdriver.Chrome(service=service, options=options)
    if DEBUG: print('initialized  webdriver...')
    #driver.fullscreen_window()
    # start at the specified URL:
    if DEBUG: print(f'\nopening browser {dt.datetime.now()}')
    driver.get(url)
    if DEBUG: print(f'got url: {url}...')
    wait = WebDriverWait(driver, 5)
    time.sleep(1)
    login_click = False
    reboot_click = False
    count_attempts = 0
    while reboot_click == False and count_attempts <= REATTEMPT_LIMIT:
        login_click = wait_login(wait, driver)
        if DEBUG & login_click: print('Login click successful...')
        reboot_click = wait_reboot(wait, driver)
        if DEBUG & reboot_click: print('Reboot click successful...')
        count_attempts += 1
        if count_attempts >= REATTEMPT_LIMIT: 
            if DEBUG: print('exceeded click attempts...')
            sys.exit(1)
    if WATCH_BROWSER: time.sleep(10) #just for visual confirmation to see that it happened
    #TODO: verify OpenDTU redirected to main page
    #TODO: if unsuccessful, trigger remedial actions
    # Close the browser instance started earlier:
    driver.quit()
        #display.stop()

    if DEBUG: print(f'browser closed {dt.datetime.now()}.')
    return reboot_click

if __name__ == '__main__':
    if DEBUG: print(f'found main...')
    if click_reset(URL):
        #TODO: notify admin by email of reboot success status
        sys.exit(0)
    else:
        #TODO: notify admin by email of reboot success status
        sys.exit(1)
