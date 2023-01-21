from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    environment = os.getenv("FLASK_ENV")
    debug = os.getenv("FLASK_DEBUG")

    # DB Settings
    secret_key = os.getenv("SECRET_KEY")    
    database_uri = os.getenv("SQLALCHEMY_DATABASE_URI")
    track_modifications = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")

    # Upload File Settings
    upload_folder = os.getenv("UPLOAD_FOLDER")
    allowed_extensions = os.getenv("ALLOWED_EXTENSIONS")

    # CKEditor Settings
    package_type = os.getenv("CKEDITOR_PKG_TYPE")
    serve_local = os.getenv("CKEDITOR_SERVE_LOCAL")
    height = os.getenv("CKEDITOR_HEIGHT")
    width = os.getenv("CKEDITOR_WIDTH")

    # Pagination Settings
    per_page: int = os.getenv("PER_PAGE")

    # Login Session TimeOut
    login_session_minutes: int = os.getenv("PERMANENT_SESSION_LIFETIME")


sett = Settings()
