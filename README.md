# SpartaHack-API-2019
The New SpartaHack API

Steps to run a local copy of SpartaHackAPI

1. Install virtualenv and virtualenvwrapper to the global python installation (source [Virtualenv and Virtualenvwrapper](http://docs.python-guide.org/en/latest/dev/virtualenvs/))  
    ```
      pip3 install virtualenv
    ```  
    ```
      pip3 install virtualenvwrapper
    ```  
   And add the following three lines to your shell startup file (.bashrc, .profile, etc.)  
    ```
      export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
      export WORKON_HOME=~/.virtualenvs
      source /usr/local/bin/virtualenvwrapper.sh
    ```  
2. Clone the API and cd into it  
3. Create a virtualenv using `mkvirtualenv` using the virtualenvwrapper  
4. Switch the python interpreter to the virtualenv using `workon virtualenv_name`  
5. Install the dependencies using `pip install -r requirements.txt`  
6. Install RabbitMQ server using `sudo apt install rabbitmq-server`  
7. With RabbitMQ server running (it will after first install otherwise run it using `sudo rabbitmq-server`)  
    ```
      sudo rabbitmqctl add_user dev mypassword
    ```  
    ```
      sudo rabbitmqctl add_vhost db_tasks
    ```  
    ```
      sudo rabbitmqctl set_user_tags dev database_tasks
    ```  
    ```
      sudo rabbitmqctl set_permissions -p db_tasks dev ".*" ".*" ".*"
    ```  
   Substitute `mypassword` with a good password and update the password in `CELERY_BROKER_URL` variable in .env file acquired in the next step
6. Get the enviorment file from Yash or Nate for accessing the important environment variables.

You're good to go!
