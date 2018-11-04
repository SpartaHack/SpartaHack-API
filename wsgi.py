from app import create_app
import os
if __name__ == '__main__':

    from dotenv import load_dotenv
    from pathlib import Path  # python3 only
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
    print(os.environ.get("FLASK_ENV"))
    app=create_app(config=os.environ.get("PROD_ENV" if os.environ.get("FLASK_ENV","")=="production" else "DEV_ENV"))

    app.run(debug=True)