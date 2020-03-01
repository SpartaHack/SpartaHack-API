.PHONY: install-dependencies dev-run prod-run help

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  install-dependencies   Install python dependencies from requirements file to the virtual enviornment"
	@echo "  dev-run                Run API in development mode"
	@echo "  prod-run               Run API in production mode"

install-dependencies:
	/home/deploy/venv/bin/pip3 install -r requirements.txt

dev-run:
	export FLASK_ENV=DEV
	/home/deploy/venv/bin/gunicorn -c /home/deploy/SpartaHackAPI/deployment/gunicornConfig.py wsgi:app &

prod-run:
	export FLASK_ENV=PROD
	/home/deploy/venv/bin/gunicorn -c /home/deploy/SpartaHackAPI/deployment/gunicornConfig.py wsgi:app &