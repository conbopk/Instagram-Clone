import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key
    SECRET_KEY = os.getenv('SECRET_KEY')

    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # GCS
    GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')

    # Upload settings
    MAX_CONTENT_LENGTH = 16*1024*1024   # 16MB max upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


