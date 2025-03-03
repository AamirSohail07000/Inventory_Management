from flask import Flask, render_template, request, redirect, url_for
from models import db, Product

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
db.init_app(app)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        category = request.form['category']

        new_product = Product(name=name, quantity=quantity, price=price, category=category)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('inventory'))

    return render_template('add_product.html')

@app.route('/inventory')
def inventory():
    products = Product.query.all()
    return render_template('inventory.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
