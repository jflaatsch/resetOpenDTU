#! Python 3.12
# reset OpenDTU
#
# by Jonathan Laatsch
# 25 Feb 2025
#
# Apache 2.0 License
#

import time, sys, os
import datetime as dt
#import keyring #NOTE: uncomment this line to use keyring after installing (pip install keyring)
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service  import Service as chrome_Service
from selenium.webdriver.firefox.service import Service as firefox_Service
#from selenium.webdriver.common.action_chains import ActionChains
#from pyvirtualdisplay import Display #NOTE: uncomment this line to use a virtual display after installing (pip install pyvirtualdisplay)
                                      #NOTE: to watch selenium execute in a window, also set WATCH_BROWSER = True
                                      #NOTE: requires additional dependencies: xserver; xephyr; xvfb; pyvirtualdisplay

#CONFIGURATION CONSTANTS
#-------------------------------
DT_FORMAT = '%Y-%m-%dT%H:%M:%SZ' #NOTE: set a custom date time format as desired
URL = f'http://192.168.189.3/maintenance/reboot' #NOTE: set your OpenDTU IP address here

#debugging options
DEBUG = False #NOTE: DEBUG = True disables reboot confirmation step for testing
DEBUG_BASH = False #NOTE: DEBUG_BASH = True disables the text prompt to complete the reboot step during testing with run_resetOpenDTU.sh or crontab
WATCH_BROWSER = False #NOTE: WATCH_BROWSER = True enables a virtual display for testing
                      #NOTE: also uncomment the pyvirtualdisplay line above to enable the display

#OpenDTU secrets storage options
SERVICE_NAME = 'OpenDTU'
USERNAME     = 'OPENDTU_USER'
PASSWORD     = 'OPENDTU_PASS'
USE_KEYRING  = 'keyring'   #NOTE: also uncomment the import keyring line above, install keyring (pip install keyring) into the virtual environment, store the password in the keyring (python setkey.py) after editing setkey.py
USE_ENV_VAR  = 'env_var'   #NOTE: store the OpenDTU username & password in ~/.profile
USE_CLR_TXT  = 'clr_txt'   #NOTE: this is NOT recommended, for clear text, store the username & password directly in the USERNAME & PASSWORD constants above
USE_SECRETS  = USE_ENV_VAR #NOTE: this will impliment the environment variable option

#selenium browser and webdriver options
USE_FIREFOX  = 'firefox'
USE_CHROMIUM = 'chromium'
USE_BROWSER  = USE_CHROMIUM #NOTE: alternatively set USE_FIREFOX to use firefox
                            #NOTE: other browsers can be used, but require additional coding
CHROMEDRIVER_PATH   = r'/usr/bin/chromedriver'
FIREFOX_BINARY_PATH = r'/usr/bin/firefox-esr'
GECKODRIVER_PATH    = r'/usr/bin/geckodriver'

#page element specifics - for easier maintenance
#NOTE: the most delicate part of selenium is finding the right page element
#NOTE: if the resetOpenDTU was working, then stops working after updating OpenDTU, the xml likely changed
#NOTE: do not change these lines unless resetOpenDTU quits working, consistently exceeds REATTEMPT_LIMIT
REBOOT_BUTTON   = '//button[text()="Reboot!"]' #reboot button (first)
REBOOT_CONFIRM  = '//button[@type="button" and text()="Reboot!"]' #confirmation button

REATTEMPT_LIMIT = 3 #NOTE: 3 or less is a reasonable limit for reattempting the website sequence reboot OpenDTU


#SELENIUM EVENT HANDLER
#-------------------------------
def wait_and_click(wait, driver, type, element):
    """
    this function finds the desired element and executes the click
    wait is the selenium method to deal with delays while waiting for websites to load

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
        print(driver.title, driver.current_url) #display the target url after clicking the element
    return None


#PAGE SECIFIC HANDLERS
#-------------------------------
def wait_login(wait, driver):
    """
    handle username & password retrieval, and login form submission

    :param wait:   WebDriverWait object
    :param driver: WebDriver object
    :return: True if successful, otherwise False
    """
    try:
        if USE_SECRETS == USE_KEYRING: #NOTE: set the desired constant above to use this option
            username = keyring.get_password(SERVICE_NAME, 'username')
            password = keyring.get_password(SERVICE_NAME, 'password')
        elif USE_SECRETS == USE_ENV_VAR:
            username = os.environ.get(USERNAME)
            password = os.environ.get(PASSWORD)
        else:
            username = USERNAME #NOTE: this is NOT recommended, this is only for testing perposes 
            password = PASSWORD #NOTE: this is NOT recommended, this is only for testing perposes

        username_element = wait.until(EC.element_to_be_clickable((By.NAME, "username")))
        username_element.clear()
        username_element.send_keys(username) #fill username
        username = None #username is no longer needed, drop it from memory

        password_element = wait.until(EC.element_to_be_clickable((By.NAME, "password")))
        password_element.clear()
        password_element.send_keys(password) #fill password
        password = None #password is no longer needed, drop it from memory

        password_element.send_keys(Keys.RETURN) #submit form
        return True

    #these exceptions did not occur in brief testing, but could be triggered if the OpenDTU interface changes
    except exceptions.ElementClickInterceptedException:
        print('login button not found...')
        return False
    except exceptions.TimeoutException:
        print('login did not appear...')
        return False


def wait_reboot(wait, driver):
    """
    handle the reboot page, click Reboot! and click Reboot! confirmation

    :param wait:   WebDriverWait object
    :param driver: WebDriver object
    :return: True if successful, otherwise False
    """
    try:
        element = REBOOT_BUTTON
        wait_and_click(wait, driver, 'xpath', element)

        element = REBOOT_CONFIRM
        if not DEBUG:
            wait_and_click(wait, driver, 'xpath', element) #this will reboot OpenDTU
            print('Wait for OpenDTU restart...') #NOTE: this is optional, comment it out if you don't want to see this confirmation in your log files
        else:
            if WATCH_BROWSER: 
                #TODO: this should select the Reboot! confirmation button for the user
                # element = wait.until(EC.element_to_be_clickable((By.XPATH, element)))
                # actions = ActionChains(driver)
                # actions.move_to_element(element).perform() #TODO: fix this syntax
                # print(f'Press enter to activate the reboot.')
                print('Click Reboot! confirmation if desired...')
                time.sleep(10) #ten seconds to click Reboot! button manually
            elif DEBUG_BASH: #NOTE: to prevent constantly interupting OpenDTU operations during testing, the actual reboot step is bypassed if DEBUG = True
                print(f'Click Reboot! confirmation is not automated in DEBUG mode.')
            else:
                #NOTE: following will cause an error in crontab implementation
                #NOTE: set the constant DEBUG_BASH = True to skip this section while testing the bash script, run_resetOpenDTU.sh
                do_click = input('yes, to reboot, NO otherwise: ')
                if do_click.lower() == 'yes':
                   wait_and_click(wait, driver, 'xpath', element)
                   print('Wait for OpenDTU restart...')
        return True

    #the following exceptions were not encountered in testing, but could occure if OpenDTU changes the website interface
    except exceptions.ElementClickInterceptedException:
        print('reset covered by another frame?...')
        return False
    except exceptions.TimeoutException:
        print(f'did not find {element}...')
        return False


#MAIN PROGRAM CONTROL
#-------------------------------
def click_reset(url):
    """
        Parameters:
            - url - source page to capture
        Return:
            - success - boolean reporting
    """
    #initiate the display window
    if WATCH_BROWSER:
        display = Display(visible= WATCH_BROWSER, size=(960, 540))
        display.start()

    # initiate the webdriver:
    #NOTE: set the USE_BROWSER constant to enable this option
    if USE_BROWSER == USE_FIREFOX:
        if DEBUG: print('loading Firefox options...')
        options = webdriver.FirefoxOptions()
        options.binary_location = CHROMEDRIVER_PATH
        options.add_argument('--headless')
        service = firefox_Service(GECKODRIVER_PATH)
        driver = webdriver.Firefox(options=options, service=service) #requires geckodriver installed
    elif USE_BROWSER == USE_CHROMIUM:
        if DEBUG: print('loading Chrome options...')
        service = chrome_Service(executable_path=CHROMEDRIVER_PATH)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        if DEBUG: print('initializing webdriver...')
        driver = webdriver.Chrome(service=service, options=options)
        if DEBUG: print('initialized  webdriver...')
    else:
        print('no webdriver configured...')
        return False
    if WATCH_BROWSER: driver.fullscreen_window()

    # start at the specified URL:
    if DEBUG: print(f'\nopening browser {dt.datetime.now()}')
    driver.get(url)
    if DEBUG:
        time.sleep(3) #wait for server response, page to load
        print(f'got url: {driver.current_url}...') #report the returned url
    wait = WebDriverWait(driver, 5)
    time.sleep(1)
    login_click = False
    reboot_click = False
    count_attempts = 0
    #loop attempts to reboot OpenDTU untill succesful or reach a set limit
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
    #TODO: check that OpenDTU restarted correctly
    #TODO: verify OpenDTU redirected to main page
    #TODO: if unsuccessful, trigger remedial actions
    # Close the browser instance started earlier:
    driver.quit()
    if WATCH_BROWSER: display.stop()

    if DEBUG: print(f'browser closed {dt.datetime.now()}.')
    return reboot_click

if __name__ == '__main__':
    if DEBUG: print(f'found main...')
    if click_reset(URL):
        #TODO: notify admin by email of reboot success status
        sys.exit(0)
    else:
        #TODO: notify admin by email of reboot failure status
        sys.exit(1)
else:
    sys.exit(0)
