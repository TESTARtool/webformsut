# webformsut
a Django webapp to  generate simple web form SUT

# Install Django on windows

### Install python and pip on Windows with chocolatey installed (http://chocolatey.org)

* open a powershell with administrator rights
* run the following commands in the administrator powershell:


*choco install python pip*

*pip install Django*

(during python/pip install accept with a yes for ALL) 

### Install python and pip on Debian/Ubuntu

sudo apt install python3 python3-pip

# How to run

## Setup (only once)

Open a terminal and clone the git repo:

*git clone https://github.com/TESTARtool/webformsut.git*

Change directory to the web app directory

*cd webformsut*

Run the following command (on windows):

*python.exe manage.py makemigrations*

*python.exe manage.py migrate*

Run the following command (on linux/mac)

*python.exe manage.py makemigrations*
*python.exe manage.py migrate*

## Running day to day 


*cd webformsut*


Run the following command (on windows):

*python.exe manage.py runserver*

Run the following command (on linux/mac)

*python manage.py runserver*

Connect to the web app using a browser e.g. :

*http://127.0.0.1/forms/nf1nl1da1*

## Updating
Stop the django test server by hitting \<ctrl>-c in the terminal window where the django process runs and 
run the following command:

*git pull*

It will download the lastest version from git.

start the server again like you would normally do.