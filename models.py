from flask_sqlalchemy import SQLAlchemy


# Initialize the database
db = SQLAlchemy()

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)  # Supports decimal values
    unit = db.Column(db.String(20), nullable=False)  # Add this line
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)

