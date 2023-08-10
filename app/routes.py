from app import app
from app.models import *
from forms import *

from flask import redirect, url_for, render_template, request


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.data.get("username")
        user = User.query.filter_by(username=username).first()

        return redirect(url_for('home', user_id=user.id))

    return render_template('login.html', form=form)


@app.route('/<int:user_id>/home')
def home(user_id):
    return render_template('home.html', user_id=user_id)


@app.route('/<int:user_id>/products')
def products(user_id):
    queryset = Product.query

    if category := request.args.get("category"):
        queryset = db.session.query(Product).join(Category).filter(Category.name == category)

    return render_template('products.html', user_id=user_id, products=queryset.all())


@app.route('/<int:user_id>/products/<int:product_id>', methods=["GET", "POST"])
def detail(user_id, product_id):
    form = AddBasketForm()
    product = Product.query.get(product_id)

    if request.method == "POST":
        cart = Cart.query.filter_by(active=True, user_id=user_id).first() or Cart(user_id=user_id)
        item = Item(product=product, cart=cart)
        db.session.add_all([cart, item])
        db.session.commit()

        return redirect(url_for('home', user_id=user_id))

    return render_template('product.html', product=product, form=form)


if __name__ == "__main__":
    app.run(debug=True)