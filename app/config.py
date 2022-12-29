from dotenv import load_dotenv
import os

load_dotenv()


class Settings():
    environment = os.getenv("FLASK_ENV")
    debug = os.getenv("FLASK_DEBUG")
    secret_key = os.getenv("SECRET_KEY")    
    database_url = os.getenv("SQLALCHEMY_DATABASE_URI")


settings = Settings()