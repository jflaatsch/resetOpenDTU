# resetOpenDTU - web automation script to reset OpenDTU through the web interface using selenium

This is a python script to use selenium webbrowser automation software to remotely reset an OpenDTU.
This initial version is intended to run on a headless Raspberry Pi.  It compromises some security to make that possible.  Some system knowledge is required to implement this solution as it is.  There is tons of room for improvement for those inclined to help the community.

Dependencies:
===================
Required:
-------------------
- python3      - commonly used coding language (reference: https://www.python.org/)
- virtualenv   - used to make a custom python environment for this project (reference: https://docs.python.org/3/library/venv.html)
- selenium     - an umbrella project for a range of tools and libraries that enable and support the automation of web browsers (reference: https://www.selenium.dev/documentation)
- crontab      - The cron command-line utility is a job scheduler on Unix-like operating systems (reference: https://en.wikipedia.org/wiki/Cron)
- chromium     - minimal web browser (alternatives: firefox, chrome, safari, edge, ie) (reference: https://www.chromium.org/Home/)
- chromedriver - web driver for selenium (alternative: geckodriver, or corresponding driver for other browsers) 

Optional:
-------------------
- keyring          - system keyring interface library for python (reference: https://pypi.org/project/keyring/)
- xserver          - GUI, X Window System display server (reference: https://www.x.org/archive/X11R7.5/doc/man/man1/Xserver.1.html)
- xephyr           - X server outputting to a window on a pre-existing X display (reference: https://www.x.org/archive/X11R7.5/doc/man/man1/Xephyr.1.html)
- xvfb             - virtual framebuffer X server for X Version 11 (reference: https://www.x.org/archive/X11R7.7/doc/man/man1/Xvfb.1.xhtml)
- pyvirtualdisplay - display driver library for python (reference: https://pypi.org/project/PyVirtualDisplay/)

Files in this repository (see Setup section below for detailed steps):
===================
main.py - main code to automate resetting OpenDTU
-------------------
this is the main script.  it is currently set to use chromium without a display and impliments user environment variables to store the OpenDTU password.  options for alternative setups are commented out.  specify the binary file locations for the browser, webdriver, and OpenDTU IP address. 32-bit Raspberry Pi might not support some dependencies

setkey.py - helper file to add the OpenDTU admin password key to your local keyring
-------------------
this file can be used to add the OpenDTU password to the system keyring. change the password, execute the script, then delete the password form this file.  

run_resetOpenDTU.sh - bash wrapper script to call from crontab
-------------------
this file handles opening the virtual environment for python and starting the script.  it also adds timestamps for the log file and can open a display for the browser on a GUI (window) operating system.

System configuration files (see Setup section below for quickstart steps):
===================
crontab - task scheduling tool to run the script at set times, command line examples 
-------------------
<code>13 03 * * 1,3,5 . $HOME/.profile; PATH/resetOpenDTU/run_resetOpenDTU.sh >> /var/log/resetOpenDTU.log 2>&1</code>
- runs OpenDTU reset script 3 days a week at 03:13 system time
- replace $HOME with the path to your home folder
- replace $PATH with the path to your installation of resetOpenDTU
- this line is intended to use environment variables set in your ~/.profile
- on Raspberry Pi, it is simpler to store secrets in the user environment variables than in the system keyring 

<code>13 03 * * * PATH/resetOpenDTU/run_resetOpenDTU.sh >> /var/log/resetOpenDTU.log 2>&1</code>
- runs OpenDTU reset script every day at 03:13 system time
- replace $PATH with the path to your installation of resetOpenDTU
- this line is intended to use the system keyring, requires modifying the baseline main.py file
- use the setkey.py helper file to set the OpenDTU key in the system keyring

$HOME/.profile - store the OpenDTU password if the system doesn't support a keyring
------------------- 
<code>export OPENDTU_USER=admin
export OPENDTU_PASS=secretpassword</code>
- these lines can be at the end of the .profile file in your home directory
- environment variables are not available to crontab by default
- use ". $HOME/.profile; " in the crontab command line (as shown above) to import the environment variables at execution time
- reference: https://pimylifeup.com/environment-variables-linux/

Setup:
===================
Install the dependencies on your system, for debian:
-------------------
<code>
apt update
apt install python3 pip crontab chromium cromedriver 
</code>
- see discussion for browser and driver alternatives
<code>
mkdir ~/resetOpenDTU
pip install virtualenv 
virtualenv ~/resetOpenDTU/.venv
cd ~/resetOpenDTU
source ./.venv/bin/activate 
pip install selenium keyring pyvirtualdisplay
deactivate
</code>
(reference: https://docs.python.org/3/library/venv.html)

Configure crontab:
-------------------
- add the appropriate crontab command line for your implimentation and edit as desired
- for initial testing, you can send the output to the terminal
<code>tty</code>
- note the output from the tty command, this is the device assigned to your terminal
<code>crontab -e</code>
- for first use of crontab select the default editor, recommend nano

- for testing you can use the following crontab command line, replacing /dev/pts/xx with the actual output of the tty command
- environment variable option for password storage:
  <code>13 03 * * 1,3,5 . $HOME/.profile; PATH/resetOpenDTU/run_resetOpenDTU.sh >> /dev/pts/xx 2>&1</code>
- keyring option for password storage:
  <code>13 03 * * * PATH/resetOpenDTU/run_resetOpenDTU.sh >> /dev/pts/xx 2>&1</code>
- replace $HOME with the actual path to your .profile for environment variables. 
- replace PATH with the actual path to your resetOpenDTU folder location
- keep the dot before $HOME, that is a command, keep the 2>&1 at the end, that directs output from the code to the terminal or log file.
- for testint purposes, return here set a time in the near future from your system clock,
- To define the time you can provide concrete values for minute (m), hour (h), day of month (dom), month (mon), and day of week (dow) or use '*' in these fields (for 'any').
- use comma separated values for multiple times, or */5 to repeat every 5 minutes for example, should be a factor of 60
- save and exit the file, if using nano: ctrl+s (save); ctrl+x (exit)

Password storage:
-------------------
Environment variables:
- this is a relatively simple and reasonably secure way to store the password for OpenDTU on your local system.  the .profile file in your home folder is loaded by the system when you - login, setting environment variables in that file will be loaded when the user logs into the system, but are not available to other users.
- the .profile file is protected such that only root and the user will be able to read the file.
<code>nano ~/.profile</code>
- add the following lines to the end of .profile 
<code>
export OPENDTU_USER=admin
export OPENDTU_PASS=secretpassword
</code>
- if you want to use a non-admin account on OpenDTU for this automation, you can change admin to the user account name
- after replacing secretpassword with your actual admin password, save and exit the file

--- OR use keyring ---

Keyring:
- this is an optional way to store your OpenDTU password for automation.  using the setkey.py helper script is not required, the keyring implementation just needs to be consistent with - the keyring retrieval used in main.py.  it might be slightly more secure to use a python commandline instead of saving a password temporarily in a file.

<code>nano setkey.py</code>
- set your admin/user password for OpenDTU by replacing the placeholder word "change" in the following line of the setkey.py file
<code>PASSWORD = 'change' #TODO: update this to the actual password when needed</code>
- after updating the password you can save it under a new name so that you can delete or shred it later without affecting setkey.py, in nano: ctrl+x. it will prompt you to save changes, press y.  it will ask for a name for the file, change it to something that will not attrack attention: temp.py

- execute the helper script with python
<code>python temp.py</code>
- delete or shred temp.py to remove the password stored in temp.py. now that the password is stored in your system keyring, temp.py is no longer needed and setkey.py will be available if you need to repeat the process
<code>rm temp.py</code>

- if you didn't change the file name, re-open setkey.py to remove the password so that it will no longer be stored in plain text
<code>nano setkey.py</code>
- after removing the password save and exit the file


Testing in one big gulp:
===================
- if everything installed correctly above, you can set the IP for OpenDTU in main.py and see if it works
  <code>nano main.py</code>
- set the IP address for OpenDTU in the CONSTANTS section near the top of the file
  <code>URL = f'http://192.168.xxx.xxx/maintenance/reboot' #NOTE: set your OpenDTU IP address here</code>
- replace 192.168.xxx.xxx with your actual OpenDTU IP address
- resetOpenDTU python script has DEBUG = False, by default, it will attempt to reset OpenDTU
- if you want to change that for the initial run and not actual reboot OpenDTU, change to DEBUG = True
- save and exit main.py

- execute the bash script run_resetOpenDTU.sh to test if it works
  <code>
  cd ~/resetOpenDTU
  ./run_resetOpenDTU.sh
  </code>
- after 30 seconds, you should get the following output:
  <code>
  start: 2025-02-25; 20:07:45, GMT
  Wait for OpenDTU restart...
  OpenDTU reset successfully...
  end : 2025-02-25; 20:08:04, GMT
  </code>
- if you get some errors, take a step back, break it down into smaller bites, or check the Troubleshooting section for quick fixes

Testing with little bites:
===================
- configuring display settings will be in a separate section for Display web browser

Configure and test main.py
-------------------
- set OpenDTU IP and DEBUG options in main.py
<code>nano main.py</code>
<code>
#CONFIGURATION CONSTANTS
#-------------------------------
DT_FORMAT = '%Y-%m-%dT%H:%M:%SZ' #NOTE: set a custom date time format as desired
URL = f'http://192.168.xxx.xxx/maintenance/reboot' #NOTE: set your OpenDTU IP address here

#debugging options
DEBUG = False #NOTE: DEBUG = True disables reboot confirmation step for testing
DEBUG_BASH = False #NOTE: DEBUG_BASH = True disables the text prompt to complete the reboot step during testing with run_resetOpenDTU.sh or crontab
WATCH_BROWSER = False #NOTE: WATCH_BROWSER = True enables a virtual display for testing
</code>
- note, DEBUG = True will not complete the reset process, OpenDTU will not restart so that it does not interupt OpenDTU's normal operation during the day
- if desired, set WATCH_BROWSER = True, this should allow you to see the OpenDTU website while the python script main.py executes
- to run a full test confirming reboot in debug mode, set DTBUG_BASH
- this will provide a user prompt, type yes to actually reboot OpenDTU

Run tests to confirm that main.py executes correctly:
- you can test the main.py script directly, then through the bash script, a crawl, walk, run approach
- to run main.py directly, activate the virtual environment
<code>
cd resetOpenDTU
source ./.venv/bin/activate
python main.py
</code>
- the script will send debug information directly to the terminal
<code>
found main...
loading Chrome options...
initializing webdriver...
initialized  webdriver...

opening browser 2025-02-25 10:26:40.980931
got url: http://192.168.189.3/maintenance/reboot...
Login click successful...
OpenDTU http://192.168.189.3/maintenance/reboot
Click Reboot! confirmation is not automated in DEBUG mode.
yes, to reboot, NO otherwise: NO
Reboot click successful...
browser closed 2025-02-25 10:26:57.505477.
</code>
- that didn't actually reboot the system, it just executed the script successfully
- when the script actually reboots OpenDTU, you should get the phrase: Wait for OpenDTU restart...
- if the script terminates with errors, check the Troubleshooting section below for solutions

Configure and test run_resetOpenDTU.sh
-------------------
- if successful, continue to the next course, execute the bash script: run_resetOpenDTU.sh
- first set DEBUG_BASH = True in main.py to prevent errors while testing the bash script
  <code>nano main.py</code>
  <code>DEBUG_BASH = True #NOTE: DEBUG_BASH = True disables the text prompt to complete the reboot step during testing with run_resetOpenDTU.sh or crontab</code>
- save the file and exit the editor
  
- match the display settings you used in main.py and modify the location of your resetOpenDTU virtual environment as required
  <code>nano run_resetOpenDTU.sh</code>
  <code>
  #export DISPLAY=":0"
  
  PYTHON_FOLDER="~/resetOpenDTU"
  </code>
- modify the PYTHON_FOLDER line to match your resetOpenDTU location
- if you enabled the display settings in main.py to watch selenium during execution, uncomment the DISPLAY line in run_resetOpenDTU.sh shown above
  <code>export DISPLAY=":0"</code>
- save the file and exit the editor
  <code>./run_resetOpenDTU.sh</code>
- that should execute without error and return the following output
  <code>
  start: 2025-02-25; 21:27:51, GMT
  found main...
  loading Chrome options...
  initializing webdriver...
  initialized  webdriver...
  
  opening browser 2025-02-25 21:28:03.896087
  got url: http://192.168.0.2/login?returnUrl=/maintenance/reboot...
  Login click successful...
  OpenDTU http://192.168.189.3/maintenance/reboot
  Click Reboot! confirmation is not automated in DEBUG mode.
  Reboot click successful...
  browser closed 2025-02-25 21:28:17.067396.
  OpenDTU reset successfully...
  end : 2025-02-25; 21:28:17, GMT
  </code>

Configure and test crontab:
-------------------
- if you already followed the crontab setup step in Setup, you will just need to set the time in the near future to see the results
  <code>crontab -e</code>
  <code>13 03 * * 1,3,5 . $HOME/.profile; PATH/resetOpenDTU/run_resetOpenDTU.sh >> /dev/pts/xx 2>&1</code>
- the resetOpenDTU command line probably starts with a coupe numbers followed by stars
- change the first number to the current minutes plus one or two, or optionally set it to repeat every few minutes, */3
- set the second number to the current hour, that should suffice
- refer to Setup to review additional crontab settings as desired
- save the file and close the editor
- in a minute you should get the same output as you did during the bash script test with run_resetOpenDTU.sh 

Finalize the setup:
-------------------
- configure crontab to output to a log file
<code>crontab -e</code>
- modify the command line to use the /var/log/resetOpenDTU.log and set the minute hour appropriately
- this example will reset OpenDTU at 03:13 on three days each week
<code>13 03 * * 1,3,5 . $HOME/.profile; PATH/resetOpenDTU/run_resetOpenDTU.sh >> /var/log/resetOpenDTU.log 2>&1</code>
- save the file and exit the editor

- modify main.py to disable DEBUG options so that resetOpenDTU will complete the reboot confirmation step
<code>nano main.py</code>
<code>
#CONFIGURATION CONSTANTS
#-------------------------------
DT_FORMAT = '%Y-%m-%dT%H:%M:%SZ' #NOTE: set a custom date time format as desired
URL = f'http://192.168.xxx.xxx/maintenance/reboot' #NOTE: set your OpenDTU IP address here

#debugging options
DEBUG = False #NOTE: DEBUG = True disables reboot confirmation step for testing
DEBUG_BASH = False #NOTE: DEBUG_BASH = True disables the text prompt to complete the reboot step during testing with run_resetOpenDTU.sh or crontab
WATCH_BROWSER = False #NOTE: WATCH_BROWSER = True enables a virtual display for testing
</code>

- confirm that run_resetOpenDTU.sh is configured to match the display option set in main.py
  <code>nano run_resetOpenDTU.sh</code>
  <code>
  #export DISPLAY=":0"
  
  PYTHON_FOLDER="~/resetOpenDTU"
  </code>

Congratulations! Working through this tutorial required dedication, but you should now have a way to reset OpenDTU on your schedule.

If you found this project useful, please add a star to help other people find it on Github. If you work with OpenDTU, please consider linking to this project from the OpenDTU Github project

Optional configuration:
===================
Use Firefox:
-------------------
- verify that you have the required binaries to run selenium with the geckodriver
  <code>
  whereis firefox
  whereis firefox-esr
  whereis geckodriver
  </code>
- note the location of the files you will need, either browser and geckodriver
- verify that the paths to the binary files are correct in main.py
  <code>nano main.py</code>
  <code>
  CHROMEDRIVER_PATH   = r'/usr/bin/chromedriver'
  FIREFOX_BINARY_PATH = r'/usr/bin/firefox-esr'
  GECKODRIVER_PATH    = r'/usr/bin/geckodriver'
  </code>

- switch the script to use firefox and geckodriver by setting USE_BROWSER in main.py as shown below
  <code>
  USE_BROWSER  = USE_FIREFOX #NOTE: alternatively set USE_CHROMIUM to use chromium/chrome
                             #NOTE: other browsers can be used, but require additional coding
  </code>

Use another browser:
-------------------
- using another browser would follow a process similar to using Firefox, but will require additional code for implimentation
- below is the relevant code, just add the corresponding options for your desired browser
- import the appropriate service as browser-service
  <code>
  from selenium.webdriver.chrome.service  import Service as chrome-service
  from selenium.webdriver.firefox.service import Service as firefox-service
  </code>
- add an option and set the path to the driver & browser as required
  <code>
  #selenium browser and webdriver options
  USE_FIREFOX  = 'firefox'
  USE_CHROMIUM = 'chromium'
  USE_BROWSER  = USE_CHROMIUM #NOTE: alternatively set USE_FIREFOX to use firefox
                              #NOTE: other browsers can be used, but require additional code for implimentation
  CHROMEDRIVER_PATH   = r'/usr/bin/chromedriver'
  FIREFOX_BINARY_PATH = r'/usr/bin/firefox-esr'
  GECKODRIVER_PATH    = r'/usr/bin/geckodriver'
  </code>
- add the desired browser opotions, service, and driver in the following section
  <code>
     # initiate the webdriver:
    #NOTE: set the USE_BROWSER constant to enable this option
    if USE_BROWSER == USE_FIREFOX:
        if DEBUG: print('loading Firefox options...')
        options = webdriver.FirefoxOptions()
        options.binary_location = CHROMEDRIVER_PATH
        options.add_argument('--headless')
        service = firefox-service(GECKODRIVER_PATH)
        driver = webdriver.Firefox(options=options, service=service) #requires >
    elif USE_BROWSER == USE_CHROMIUM:
        if DEBUG: print('loading Chrome options...')
        service = chrome-service(executable_path=CHROMEDRIVER_PATH)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        if DEBUG: print('initializing webdriver...')
        driver = webdriver.Chrome(service=service, options=options)
        if DEBUG: print('initialized  webdriver...')
    else:
        print('no webdriver configured...')
        return False
  </code>

Use keyring:
-------------------
- configuring resetOpenDTU to use the keyring library to store the OpenDTU password is described in Setup above

Show the browser window in an xwindow display:
-------------------
- if the system does not already have an xwindow GUI display, implementing the the browser in a display will require significant additional resources
- TODO: walk through settings for enabling the xwindow display for testing

Discussion:
===================
this script requires some understanding of python, selenium, and crontab to impliment fully.  there are several options and the script can be modified to meet your requirements by changing a few constants in main.py.

Password storage options - keyring or environment variables, other methods are also possible but will require more modification to main.py
-------------------
- during automation testing, OpenDTU responded with a login screen. you will need to store the password for an OpenDTU user for the automated script to get past the login.
- the script was developed for keyring, then finally implimented with environment variables on Raspberry Pi
- keyring may be more secure, but it is problematic on a Raspeberry Pi (reference: https://pypi.org/project/keyring/ and https://www.geeksforgeeks.org/storing-passwords-with-python-keyring/)
- choose one of the other or find another solution so that you don't have to store the password as plain text
- for a good discussion of other options, reference: https://stackoverflow.com/questions/7014953/i-need-to-securely-store-a-username-and-password-in-python-what-are-my-options

Selenium browser and webdriver options - several available
-------------------
- selenium needs a full web browser installed to operate
- selenium also needs the corresponding driver to interface with the browser
- Firefox uses geckodriver, Chrome and Chromium use chromedriver
- other browsers available, but will require more modification to the current script: Safari; Edge; IE
- your decision will probably depend on what you already have installed and are familiar with
- for complete details reference: https://www.selenium.dev/documentation/webdriver/


Troubleshooting:
===================
Installation issues:
-------------------
- -bash: virtualenv: command not found
  - there are multiple ways to setup the virtual environment, you can use a method that is already installed or install virtualenv
  <code>pip install virtualenv</code>

- The virtual environment was not created successfully because ensurepip is not available.  On Debian/Ubuntu systems, you need to install the python3-venv package using the following command.
  - there are multiple ways to setup the virtual environment, you must have tried the python -m venv method, but python3-venv is not installed
  <code>apt install python3-venv</code>

- raise child_exception_type(errno_num, err_msg, err_filename) FileNotFoundError: [Errno 2] No such file or directory: 'Xephyr'
  - apt install xserver-xephyr
  - will need 163MB for installation
  - if you intend to use the script without display, remove the requirement for Xephyr from main.py
  - comment out reference to pyvirtualdisplay and to Display

- FileNotFoundError: [Errno 2] No such file or directory: 'Xvfb'
  - install xvfb: apt install xvfb

Display configuration issues:
-------------------
- pyvirtualdisplay.abstractdisplay.XStartError: Xephyr program closed. command: ['Xephyr', '-br', '-screen', '960x540x24', '-displayfd', '4', '-resizeable'] stderr: b'\nXephyr cannot open host display. Is DISPLAY set?\n'
  - if you intend to use the script without display, remove the requirement for Xephyr from main.py
  - comment out reference to pyvirtualdisplay and to Display
  - fixing this can be involved, if required for testing, install the optional dependencies to watch selenium interact with the browser
  - if this error occurs while executing run_resetOpenDTU.sh, execute main.py directly from python with the virtual environment activated: source ./.venv/bin/activate && python main.py
  - if that works correctly, check the settings in run_resetOpenDTU.sh, uncomment the line: export DISPLAY=":0"
  - reference external sources for which value to set for DISPLAY

Selenium configuration issues:
-------------------
- selenium.common.exceptions.WebDriverException: Message: Unsupported platform/architecture combination: linux/aarch64
  - this error occurs when selenium doesn't receive a path to a binary file for the browser or webdriver
  - specify the location of the binary executables of the browser and webdriver
  - locate the required binary files for your desired configuration:
    - whereis chromium;
    - whereis chromedriver;
    - whereis firefox;
    - whereis geckodriver
  - add the path to the corresponding lines in main.py
  <code>
  CHROMEDRIVER_PATH = r'/usr/bin/chromedriver'
  FIREFOX_BINARY_PATH = r'/usr/bin/firefox-esr'
  GECKODRIVER_PATH = r'/usr/bin/geckodriver'
  </code>
  - modify the path contants to match the paths returned by whereis

- selenium.common.exceptions.NoSuchDriverException: Message: Unable to obtain driver for chrome; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors/driver_location
  - ensure that main.py is configured to use the selenium webdriver which is installed on your system: options; server; webdriver; & paths to binary files
  - firefox/firefox-esr use the geckodriver
  - chrome/chromium use the chromedriver
  - install the required browser and driver:
    - apt install firefox
    - firefox should include geckodriver, reference: https://www.baeldung.com/linux/geckodriver-installation
    - apt install chromium-browser chromium-chromedriver
  - 
  - search for external documentation if you intend to use another browser/webdriver combination

- selenium.common.exceptions.SessionNotCreatedException: Message: Unable to find a matching set of capabilities
  - ensure that main.py is configured to use the selenium webdriver which is installed on your system: options; server; webdriver; & paths to binary files
  - firefox/firefox-esr use the geckodriver
  - chrome/chromium use the chromedriver

- selenium.common.exceptions.InvalidArgumentException: Message: binary is not a Firefox executable
- Message: binary is not a Firefox executable - firefox is either not installed, or the path to the executable is incorrect
  - install firefox: apt install firefox
  - update path to executable: whereis firefox
  - you might have firefox-esr install, you can also use that
  - optionally install firefox-esr ~400MB required for installation with dependencies: apt install firefox-esr
  - update path to executable: whereis firefox-esr
  - see selenium.common.exceptions.WebDriverException above

- selenium.common.exceptions.NoSuchDriverException: Message: Unable to obtain driver for chrome; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors/driver_location
  - install chrome: apt install chrome-browser
  - note that chrome is resource intensive, if it is not already installed, you may want to use chromium instead
  - update path to executable: whereis google-chrome; whereis chromebrowser
  - see selenium.common.exceptions.WebDriverException above

Execution errors:
-------------------
- selenium.common.exceptions.WebDriverException: Message: Failed to decode response from marionette
  - selenium was not able to read the server response or no response from the server
  - this could be caused by the browser not being able to access OpenDTU through the network
  - open a regular browser and attemp to connect to OpenDTU
  - if no GUI installed attempt to reach OpenDTU by other means: ping; wget; curl
  - use gunzip or similar to decode the binary response
  - the text in the response will likely state that JavaScript is required
  - if it persists, search for external references to assist with resolving the error
  - please submit the your solution as a bug report to be added to the documentation
  - 
- keyring.errors.NoKeyringError: No recommended backend was available. Install a recommended 3rd party backend package; or, install the keyrings.alt package if you want to use the non-recommended backends. See https://pypi.org/project/keyring for details.
  - this is likely on Raspberry Pi, no system keyring recognized by python's keyring library
  - attempt to install an alternative system keyring that will work with python's keyring
  - alternatively, use environment variables to store the OpenDTU password on the local system
  - additionally reference: https://pypi.org/project/keyring/ and https://www.geeksforgeeks.org/storing-passwords-with-python-keyring/
  - reference: https://stackoverflow.com/questions/7014953/i-need-to-securely-store-a-username-and-password-in-python-what-are-my-options
  - some options require dbus, if you get those to work on Raspberry Pi, please contribution to the documentation through a bugreport or pull request
  - deb-keyring was unsuccessful
  - gnome-keyring was unsuccessful
 
- keyring.errors.KeyringLocked: Failed to unlock the collection!
  - keyring configuration on Raspberry Pi still incompatable, consider using environment variables instead
  - if you get a keyring implementation to work on Raspberry Pi, please contribute to the documentation through a bugreport or pull request

- Command.SEND_KEYS_TO_ELEMENT, {"text": "".join(keys_to_typing(value)), "value": keys_to_typing(value)}, line 137, in keys_to_typing characters.extend(val), TypeError: 'NoneType' object is not iterable
  - the login username or password is not getting into python correctly
  - check that the environment variables are set in ~/.profile as described in Setup.
  - if the script executes correctly directly from python, but this occurs when using the bash script run_resetOpenDTU.sh, check that the environment variables are being loaded correctly in the following line:
  <code>13 03 * * 1,3,5 . $HOME/.profile; PATH/resetOpenDTU/run_resetOpenDTU.sh >> /var/log/resetOpenDTU.log 2>&1</code>
  - keep the dot/period before the $HOME directly.  the dot tells bash to execute/load the ~/.profile with the environment variables
  - replace $HOME with your actual home path and replace PATH with the actual path to resetOpenDTU

- do_click = input('yes, to reboot, NO otherwise: '), EOFError: EOF when reading a line
  - this probably occured while executing the bash script, run_resetOpenDTU.sh.  it is not possible to interact with the python script through the bash script in this way.  you will not be able to complete the reboot confirmation step as configured during testing.
  - comment out the following lines during bash script testing:
  <code>
                # following will cause an error in crontab implementation
                #do_click = input('yes, to reboot, NO otherwise: ')
                #if do_click.lower() == 'yes':
                #   wait_and_click(wait, driver, 'xpath', element)
                #   print('Wait for OpenDTU restart...')
  </code>

Another hint:
-------------------
- if multiple versions of python are installed on the system, pay attention to which version is running in the virtual environment


