import os
def load_env_variables():
    from dotenv import load_dotenv
    load_dotenv()

class BaseConfig:
    DEBUG=False
    TESTING=False
    SECRET_KEY=os.getenv("SECRET_KEY")

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    DATABASE_URL=os.getenv("DEV_DATABASE_URL")


class ProdConfig(BaseConfig):
    DEBUG = False
    DATABASE_URL=os.getenv("PROD_DATABASE_URL")

