# SpartaHack-API-2019
The New SpartaHack API

Steps to run a local copy of SpartaHackAPI

1. Install virtualenv and virtualenvwrapper to the global python installation (source [Virtualenv and Virtualenvwrapper](http://docs.python-guide.org/en/latest/dev/virtualenvs/))  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`pip install virtualenv`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`pip install virtualenvwrapper`  
   And add the following three lines to your shell startup file (.bashrc, .profile, etc.)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`export WORKON_HOME=~/.virtualenvs`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`source /usr/local/bin/virtualenvwrapper.sh`  
2. Clone the API and cd into it
3. Create a virtualenv using `mkvirtualenv` using the virtualenvwrapper
4. Switch the python interpreter to the virtualenv using `workon virtualenv_name` 
5. Install the dependencies using `pip install -r requirements.txt`
6. Get the enviorment file from Yash or Nate for accessing the important environment variables.

You're good to go!
