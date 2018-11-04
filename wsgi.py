from app import create_app
import os
from config import load_env_variables
if __name__ == '__main__':

    load_env_variables()
    app=create_app(config=os.environ.get("PROD_ENV" if os.environ.get("FLASK_ENV","")=="production" else "DEV_ENV"))

    app.run(debug=True)