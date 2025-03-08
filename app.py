from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config import SECRET_KEY
import os
from sqlalchemy import text
# Initialize Flask app
app = Flask(__name__)
# app.secret_key = SECRET_KEY

app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback_secret_key")
# Load database configuration from config.py
app.config.from_pyfile("config.py")

# Initialize SQLAlchemy with Flask app
db = SQLAlchemy(app)
from models import Product

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each product
    name = db.Column(db.String(100), nullable=False)  # Product name (required)
    quantity = db.Column(db.Float, nullable=False)  # Available stock quantity (supports decimals)
    unit = db.Column(db.String(10), nullable=False)  # Unit of measurement (pcs/kg)
    price = db.Column(db.Float, nullable=False)  # Product price
    category = db.Column(db.String(50), nullable=False)  # Product category

# Route: Home Page
@app.route('/')
def home():
    return render_template('index.html')  # Renders the homepage

# Route: Display Inventory (Product List)
@app.route('/inventory')
def inventory():
    category = request.args.get("category", "").strip().lower()  # Normalize category input
    
    # Fetch all unique categories for the filter dropdown
    categories = sorted(set([c.category for c in Product.query.all()]))  

    # Apply filter only if a category is selected
    if category:
        products = Product.query.filter(Product.category.ilike(category)).all()
    else:
        products = Product.query.all()

    return render_template("inventory.html", products=products, categories=categories)

# Route: Add Product (GET - Show Form, POST - Handle Submission)
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form.get('name').strip() #Remove leading?trailing spaces
        quantity = request.form.get('quantity')
        unit = request.form.get('unit')
        price = request.form.get('price')
        category = request.form.get('category')

        # Validate input fields
        if not name or not quantity or not unit or not price or not category:
            flash("All fields are required!", "danger")

        else:
            try:
                quantity = float(quantity)  # Convert quantity to float
                price = float(price)  # Convert price to float
                # Check if the product already exists
                existing_product = Product.query.filter_by(name=name, unit=unit, category=category).first()
                
                if existing_product:
                    # If product exists, update the quantity instead of adding a duplicate
                    existing_product.quantity += quantity
                    existing_product.price = price  # Optionally update the price
                    db.session.commit()
                    flash(f"Updated quantity for existing product: {name} ({quantity} {unit})!", "success")
                else:
                    # Add new product with a unique ID
                    new_product = Product(name=name, quantity=quantity, unit=unit, price=price, category=category)
                    db.session.add(new_product)
                    db.session.commit()
                    flash(f"Product '{name}' added successfully!", "success")

            except ValueError:
                    flash("Invalid number format for quantity or price.", "danger")

    # Stay on the same page after submission
    return render_template('add_product.html')
@app.route('/delete_product/<int:id>', methods=['GET'])
def delete_product(id):
    product = Product.query.get(id)  # Fetch product by ID
    if product:
        db.session.delete(product)
        db.session.commit()
        flash(f"Product '{product.name}' deleted successfully!", "success")
    else:
        flash("Product not found!", "danger")

    return redirect(url_for('inventory'))  # Redirect back to inventory page

# Clear Inventory action
@app.route('/clear_inventory', methods=['POST'])
def clear_inventory():
    try:
        # Step 1: Delete all products
        db.session.query(Product).delete()
        db.session.commit()

        # Step 2: Reset AUTO_INCREMENT to 101
        db.session.execute(text("ALTER TABLE product AUTO_INCREMENT = 101"))
        db.session.commit()

        flash("Inventory cleared successfully!", "success")
    except Exception as e:
        db.session.rollback()
        print("Error:", e)  # Print the actual error in the console
        flash(f"Error clearing inventory! {str(e)}", "danger")

    return redirect(url_for('inventory'))  # Redirect back to inventory page


# Run Flask App
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure tables exist before running
    app.run(debug=True)
