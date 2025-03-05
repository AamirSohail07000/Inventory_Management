import os
from dotenv import load_dotenv # type: ignore
# MySQL Database Configuration
load_dotenv()

# SQLAlchemy Connection String (Uses pymysql)
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking to save resources


SECRET_KEY = "mbc123456"
