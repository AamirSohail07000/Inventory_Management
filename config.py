import os
from dotenv import load_dotenv # type: ignore
# MySQL Database Configuration
load_dotenv()

# SQLAlchemy Connection String (Uses pymysql)
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:786123%40Ms@127.0.0.1/mbctraders_inventorydb'
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking to save resources


SECRET_KEY = "mbc123456"
