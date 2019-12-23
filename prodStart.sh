export FLASK_ENV = "PROD"

gunicorn -c gunicornConfig.py wsgi:app