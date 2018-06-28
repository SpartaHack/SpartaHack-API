import os

def load_env_variables(): #To load the config varibles before creating the flask object
    from dotenv import load_dotenv
    load_dotenv()

#To load config variables from object.
class BaseConfig:
    DEBUG=False
    TESTING=False
    SECRET_KEY=os.getenv("SECRET_KEY")
    CELERY_BROKER_URL=os.getenv("CELERY_BROKER_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI=os.getenv("DEV_DATABASE_URL")


class ProdConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI=os.getenv("PROD_DATABASE_URL")

