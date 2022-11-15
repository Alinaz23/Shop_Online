from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from cloudipsp import Api, Checkout


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return self.text


@app.route('/buy/<int:id>')
def item_buy(id):
    item = Item.query.get(id)

    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": str(item.price) + "00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect (url)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/product')
def product():
    items = Item.query.order_by(Item.price).all()
    return render_template('product.html', data=items)


@app.route('/product/<int:id>/del')
def product_del(id):
    item = Item.query.get_or_404(id)

    try:
        db.session.delete(item)
        db.session.commit()
        return redirect('/product')
    except:
        return "При удалении товара произошла ошибка"


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create', methods=['POST','GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        text = request.form['text']

        item = Item(title=title, price=price, text=text)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return 'Ошибка'
    else:
        return render_template('create.html')

if __name__=='__main__':
    app.run(debug=True)
