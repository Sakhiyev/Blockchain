from flask import Flask, render_template, request, redirect , url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from cloudipsp import Api, Checkout


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.String(100))

    def __repr__(self):
        return self.title


@app.route('/')
def index():
    items = Item.query.order_by(Item.id.desc()).all()
    return render_template('index.html', data=items)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/products')
def products():
    articles = Item.query.order_by(Item.id.desc()).all()
    return render_template('products.html', articles=articles)


@app.route('/products/<int:id>')
def products_detail(id):
    article = Item.query.get(id)
    return render_template('products_detail.html', article=article)


@app.route('/buy/<int:id>')
def item_buy(id):
    item = Item.query.get(id)
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": str(item.price)+"0"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


@app.route('/buy2/<int:id>')
def item_buy2(id):
    item = Item.query.get(id)
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": str(item.price)+"0"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']
        isActive = request.form['isActive']
        item = Item(title=title, price=price, isActive=isActive)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/products')
        except:
            return "Получилась ошибка"
    else:
        return render_template('create.html')


if __name__ == "__main__":
     app.run(debug=True)