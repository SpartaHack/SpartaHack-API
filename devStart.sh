export FLASK_ENV = "DEV"

gunicorn -c gunicornConfig.py wsgi:app