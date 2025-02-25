# resetOpenDTU - web automation script to reset OpenDTU through the web interface using selenium

This is a python script to use selenium webbrowser automation software to remotely reset an OpenDTU.
This initial version is intended to run on a headless Raspberry Pi.  It compromises some security to make that possible.  Some system knowledge is required to implement this solution as it is.  There is tons of room for improvement for those inclined to help the community.

Dependencies:
===================
Required:
-------------------
python3      - commonly used coding language
selenium     - website manipulation library for python
crontab      - task scheduling tool to auto initiate the script
chromium     - web browser (alternatives: firefox, chrome)
chromedriver - web driver for selenium (alternative: geckodriver)

Optional:
-------------------
keyring          - system keyring interface library for python
pyvirtualdisplay - display driver library for python

Files in this repository (see Setup section below for quickstart steps):
===================
main.py - main code to automate resetting OpenDTU
-------------------
this is the main script.  it is currently set to use chromium without a display and impliments user environment variables to store the OpenDTU password.  options for alternative setups are commented out.  specify the binary file locations for the browser, webdriver, and OpenDTU IP address. 32-bit Raspberry Pi might not support some dependencies

setkey.py - helper file to add the OpenDTU admin password key to your local keyring
-------------------
this file can be used to add the OpenDTU password to the system keyring. change the password, execute the script, then delete the password form this file.  

run_resetOpenDTU.sh - bash wrapper script to call from crontab
-------------------
this file handles opening the virtual environment for python and starting the script.  it also adds timestamps for the log file and can  open a display for the browser on a GUI (window) operating system.

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
<code>
export OPENDTU_USER=admin
export OPENDTU_PASS=secretpassword
</code>
- these lines can be at the end of the .profile file in your home directory
- environment variables are not available to crontab by default
- use ". $HOME/.profile; " in the crontab command line (as shown above) to import the environment variables at execution time
- reference: https://pimylifeup.com/environment-variables-linux/

Setup:
===================
install the dependencies on your system, for debian:
<code>
apt update
apt install python3 pip crontab chromium cromedriver 
</code>
- see discussion for browser and driver alternatives
<code>
mkdir resetOpenDTU
cd resetOpenDTU
python -m venv .venv 
source ./.venv/bin/activate 
pip install selenium pyvirtualdisplay keyring
deactivate
</code>
(reference: https://docs.python.org/3/library/venv.html)

- add the appropriate crontab command line for your implimentation and edit as desired
- for initial testing, you can send the output to the terminal
<code>tty</code>
- note the output from the tty command, this is the device assigned to your terminal
<code>crontab -e</code>
- for first use of crontab select the default editor, recommend nano

- for testing you can use the following crontab command line, replacing /dev/pts/xx with the actual output of the tty command
<code>13 03 * * 1,3,5 . $HOME/.profile; PATH/resetOpenDTU/run_resetOpenDTU.sh >> /dev/pts/xx 2>&1</code>
- replace $HOME with the actual path to your .profile for environment variables. 
- replace PATH with the actual path to your resetOpenDTU folder location
- keep the dot before $HOME, that is a command, keep the 2>&1 at the end, that directs output from the code to the terminal or log file.
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
this is an optional way to store your OpenDTU password for automation.  using the setkey.py helper script is not required, the keyring implementation just needs to be consistent with the keyring retrieval used in main.py.  it might be slightly more secure to use a python commandline instead of saving a password temporarily in a file.

<code>
nano setkey.py
</code>

set your admin/user password for OpenDTU by replacing the placeholder word change in the following line of the setkey.py file
<code>
PASSWORD = 'change' #TODO: update this to the actual password when needed
</code>
after updating the password you can save it under a new name so that you can delete or shred it later without affecting setkey.py, in nano: ctrl+x. it will prompt you to save changes, press y.  it will ask for a name for the file, change it to something that will not attrack attention: temp.py

execute the helper script with python
<code>
python temp.py
</code>
delete or shred temp.py to remove the password stored in a the file. now that the password is stored in your system keyring, temp.py is no longer needed and setkey.py will be available if you need to repeat the process

if you didn't change the file name, re-open setkey.py to remove the password so that it will no longer be stored in plain text
<code>
nano setkey.py
</code>
after removing the password save and exit the file

Testing:
-------------------
- set DEBUG = True in main.py
- TODO: add code steps
- if desired, set WATCH_BROWSER = True
- TODO: add code steps
- run tests to confirm that main.py executes correctly
- you can test the main.py script directly, or through the bash script
- to run main.py directly, activate the virtual environment
<code>
source ~/resetOpenDTU/.venv/bin/activate
python main.py
</code>


Work out any kinks to get the script to run reliably with OpenDTU, then finalize the setup:
-------------------
- configure crontab to output to a log file
<code>crontab -e</code>
- modify the command line to use the /var/log/resetOpenDTU.log
<code>13 03 * * 1,3,5 . $HOME/.profile; PATH/resetOpenDTU/run_resetOpenDTU.sh >> /var/log/resetOpenDTU.log 2>&1</code>
- save and exit the file

- modify main.py to turn off debugging mode so that it will complete the reboot confirmation step
<code>nano main.py</code>
- change the constant DEBUG = False, so that it will not output troubleshooting steps and compelte the reboot confirmation step
<code>DEBUG = False #NOTE: DEBUG = True disables reboot confirmation step for testing</code>
- change the constant WATCH_BROWSER = False, to minimize system resources, or prepare for headless operation
<code>WATCH_BROWSER = False</code>

Discussion:
===================
this initial script requires some understanding of python, selenium, and crontab to impliment fully.  there are several options and the script can be modified to meet your requirements.

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


