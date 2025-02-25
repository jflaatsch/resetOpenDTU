# resetOpenDTU - web automation script to reset OpenDTU through the web interface using selenium

This is a python script to use selenium webbrowser automation software to remotely reset an OpenDTU.
This initial version is intended to run on a headless Raspberry Pi.  It compromises some security to make that possible.  Some system knowledge is required to implement this solution as it is.  There is tons of room for improvement for those inclined to help the community.

Dependencies:
-------------------
python3
selenium
crontab - to auto initiate the script
chromium (alternatives: firefox, chrome)
chromedriver (alternative: geckodriver)

Optional:
-------------------
keyring
pyvirtualdisplay

Files:
-------------------

main.py - main code to automate resetting OpenDTU
-------------------
this is the main script.  it is currently set to use chromium without a display and impliments user environment variables to store the OpenDTU password.  options for alternative setups are commented out.  older 32-bit Raspberry Pi may not support chromium or other dependencies

setkey.py - helper file to add the OpenDTU admin password key to your local keyring
-------------------
this file can be used to add the OpenDTU password to the system keyring. change the password, execute the script, then change then delete the password again.  

run_resetOpenDTU.sh - wrapper file to call from crontab
-------------------
this file handles open the virtual environment for python and starting the script.  it also adds timestamps for the log file and can handle opening the display if you want to see the browser on a GUI (window) operating system

crontab - task scheduling tool to run the script at set times, command line examples 
-------------------
13 03 * * 1,3,5 . $HOME/.profile; PATH/resetOpenDTU/run_resetOpenDTU.sh >> /var/log/resetOpenDTU.log 2>&1
- runs OpenDTU reset script 3 days a week at 03:13 system time
- replace $HOME with the path to your home folder
- replace $PATH with the path to your installation of resetOpenDTU
- this line is intended to use environment variables set in your ~/.profile
- on Raspberry Pi, it is simpler to store secrets in the user environment variables than in the system keyring 

13 03 * * * PATH/resetOpenDTU/run_resetOpenDTU.sh >> /var/log/resetOpenDTU.log 2>&1
- runs OpenDTU reset script every day at 03:13 system time
- replace $PATH with the path to your installation of resetOpenDTU
- this line is intended to use the system keyring, requires modifying the baseline main.py file
- use the setkey.py helper file to set the OpenDTU key in the system keyring

$HOME/.profile - store the OpenDTU password if the system doesn't support a keyring
-------------------
- export OPENDTU_USER=admin
- export OPENDTU_PASS=secretpassword

- these lines can be at the end of the .profile file in your home directory
- environment variables are not available to crontab by default
- use ". $HOME/.profile; " in the crontab command line (as shown above) to import the environment variables at execution time
- reference: https://pimylifeup.com/environment-variables-linux/

Setup:
-------------------
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
</code>

<code>
crontab -e
</code>

(first use select the default editor, nano)
add the appropriate crontab command line for your implimentation and edit as desired
(for testing you can send the output to the terminal, from a command line type tty, it will report the terminal as "/dev/pts/xx" put that in place of the log file, keep the "2>&1")
ctrl+s (save), ctrl+x (exit)

work out the kinks to get it to run reliably, then finalize the setup!

Discussion:
-------------------
this initial script requires some understanding of python, selenium, and crontab to impliment fully.  there are several options and the script can be modified to meet your requirements.

Password storage options - keyring or environment variables
-------------------
- the script was developed for keyring, then finally implimented with environment variables on Raspberry Pi
- keyring may be more secure, but it is problematic on a Raspeberry Pi (reference: https://pypi.org/project/keyring/)
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


