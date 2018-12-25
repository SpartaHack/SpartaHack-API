if __name__ == '__main__':

    from dotenv import load_dotenv
    from pathlib import Path  # python3 only
    env_path = Path('.') / '.env'
    load_dotenv(verbose=True,dotenv_path=env_path)
    from app import create_app
    import os
    if os.getenv("FLASK_ENV") == "DEV":
        config = "DevelopmentConfig"
    else:
        config = "ProdConfig"
    app=create_app(config)
    app.run(debug=app.config.get("DEBUG",False))