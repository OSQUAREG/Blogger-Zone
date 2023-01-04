from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    environment = os.getenv("FLASK_ENV")
    debug = os.getenv("FLASK_DEBUG")
    secret_key = os.getenv("SECRET_KEY")    
    database_url = os.getenv("SQLALCHEMY_DATABASE_URI")
    access_token_expires = os.getenv("JWT_ACCESS_TOKEN_EXPIRES_MINUTES")
    refresh_token_expires = os.getenv("JWT_REFRESH_TOKEN_EXPIRES_DAYS")
    upload_folder = os.getenv("UPLOAD_FOLDER")
    allowed_extensions = os.getenv("ALLOWED_EXTENSIONS")


settings = Settings()
