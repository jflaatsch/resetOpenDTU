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
<code>
13 03 * * 1,3,5 . $HOME/.profile; PATH/resetOpenDTU/run_resetOpenDTU.sh >> /var/log/resetOpenDTU.log 2>&1
</code>
- runs OpenDTU reset script 3 days a week at 03:13 system time
- replace $HOME with the path to your home folder
- replace $PATH with the path to your installation of resetOpenDTU
- this line is intended to use environment variables set in your ~/.profile
- on Raspberry Pi, it is simpler to store secrets in the user environment variables than in the system keyring 

<code>
13 03 * * * PATH/resetOpenDTU/run_resetOpenDTU.sh >> /var/log/resetOpenDTU.log 2>&1
</code>
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
apt install python3 pip crontab chromium cromedriver (see discussion for browser and driver alternatives)
</code>

<code>
mkdir resetOpenDTU
cd resetOpenDTU
python -m venv .venv (reference: https://docs.python.org/3/library/venv.html)
source ./.venv/bin/activate 
pip install selenium pyvirtualdisplay keyring
deactivate
</code>

add the appropriate crontab command line for your implimentation and edit as desired
for initial testing, you can send the output to the terminal
<code>tty</code> note the output from the tty command, this is the device assigned to your terminal
<code>crontab -e</code>(first use select the default editor, recommend nano)
for testing you can use the following crontab command line, replacing /dev/pts/xx with the actual output of the tty command
<code>13 03 * * 1,3,5 . $HOME/.profile; PATH/resetOpenDTU/run_resetOpenDTU.sh >> /dev/pts/xx 2>&1</code> (keep the dot before $HOME and keep the 2>&1 at the end)
replace $HOME with the actual path to your .profile for environment variables. 
replace PATH with the actual path to your resetOpenDTU folder location
keep the dot before $HOME, that is a command, keep the 2>&1 at the end, that directs output from the code to the terminal or log file.
save and exit: ctrl+s (save), ctrl+x (exit)

Password storage:
-------------------
Environment variables:
- this is a relatively simple and reasonably secure way to store the password for OpenDTU on your local system.  the .profile file in your home folder is loaded by the system when you - login, setting environment variables in that file will be loaded when the user logs into the system, but are not available to other users.
- the .profile file is protected such that only root and the user will be able to read the file.
<code>nano ~/.profile</code>
add the following lines to the end of .profile 
<code>
export OPENDTU_USER=admin
export OPENDTU_PASS=secretpassword
</code>
if you want to use a non-admin account on OpenDTU for this automation, you can change admin to the user account name
after replacing secretpassword with your actual admin password, save and exit the file

--- OR use keyring ---

Keyring:
this is an optional way to store your OpenDTU password for automation.  using the setkey.py helper script is not required, the keyring implementation just needs to be consistent with the keyring retrieval used in main.py

<code>
nano setkey.py
</code>

set your admin/user password for OpenDTU by replacing the placeholder word change in the following line of the setkey.py file
<code>
PASSWORD = 'change' #TODO: update this to the actual password when needed
</code>
after updating the password save and close the file, ctrl+s (save), ctrl+x (exit)

execute the script with python
<code>
python setkey.py
</code>

re-open setkey.py to remove the password so that it will no longer be stored in plain text
<code>
nano setkey.py
</code>
after removing the password save and close the file, ctrl+s (save), ctrl+x (exit)




work out the kinks to get it to run reliably, then finalize the setup!

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


