from dotenv import load_dotenv
import os
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
    TESTING = True
DATABASE_URL=os.getenv("PROD_DATABASE_URL")

