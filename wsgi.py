import os
from app import create_app

if __name__ == '__main__':

    from dotenv import load_dotenv
    from pathlib import Path  # python3 only
    env_path = Path('.') / '.env'
    load_dotenv(verbose=True,dotenv_path=env_path)
    app=create_app("DevelopmentConfig")
    app.run(debug=True)