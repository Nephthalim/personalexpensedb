from flask import Flask, request, jsonify, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init DataBase
db = SQLAlchemy(app)

# Init Class
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, date, price, qty):
        self.name = name
        self.price = price
        self.qty = qty

# Post item
@app.route('/', methods=['POST'])
def add_item():
    name = request.form['name']
    price = request.form['price']
    qty = request.form['qty']

    new_item = Item(name, None, price, qty)
    try:
        db.session.add(new_item)
        db.session.commit()
        return redirect('/')
    except:
        print("Problem: Could not add to db")


# Get All items
@app.route('/', methods=['GET'])
def get_items():
    items = Item.query.all()
    return render_template('index.html', items=items)

# Get Single item
def get_item(id):
    return Item.query.get(id)
    

# Update a item
@app.route('/update_item/<id>', methods=['GET', 'POST'])
def update_item(id):
    item = get_item(id)

    if request.method == 'POST':

        item.name = request.form['name']
        item.price = request.form['price']
        item.qty = request.form['qty']

        db.session.commit()

        return redirect('/')

    else:
        return render_template('update.html', item=item)
        


# Delete item


@app.route('/delete_item/<id>')
def delete_item(id):
    item_to_delete = Item.query.get(id)
    db.session.delete(item_to_delete)
    db.session.commit()
    return redirect('/')


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
