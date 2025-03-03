from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Database Configuration (Using SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)

# Route: Home Page
@app.route('/')
def home():
    return 'Inventory Management'

# Route: Display Inventory (Product List)
@app.route('/inventory')
def inventory():
    products = Product.query.all()  # Fetch all products from the database
    return render_template('inventory.html', products=products)

# Route: Add Product (GET - Show Form, POST - Handle Submission)
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        category = request.form['category']

        # Create a new Product instance
        new_product = Product(name=name, quantity=quantity, price=price, category=category)

        # Add and commit to the database
        db.session.add(new_product)
        db.session.commit()

        # Redirect to inventory page after adding the product
        return redirect(url_for('inventory'))

    return render_template('add_product.html')

# Run Flask App
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
