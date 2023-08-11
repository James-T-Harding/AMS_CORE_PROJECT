from app import app
from app.models import *
from forms import *

from flask import redirect, url_for, render_template, request


def render_nav(template, user_id, **kwargs):
    kwargs.update(user_id=user_id)
    kwargs["home_url"] = url_for('home', user_id=user_id)
    kwargs["products_url"] = url_for('products', user_id=user_id)
    kwargs["basket_url"] = url_for('basket', user_id=user_id)

    return render_template(template, **kwargs)


def get_or_create(model, **kwargs):
    if result := model.query.filter_by(**kwargs).first():
        return result

    item = model(**kwargs)
    db.session.add(item)
    db.session.commit()

    return item


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
    return render_nav('home.html', user_id)


@app.route('/<int:user_id>/products')
def products(user_id):
    queryset = Product.query

    if category := request.args.get("category"):
        queryset = db.session.query(Product).join(Category).filter(Category.name == category)

    return render_nav('products.html', user_id, products=queryset.all())


@app.route('/<int:user_id>/products/<int:product_id>', methods=["GET", "POST"])
def detail(user_id, product_id):
    product = Product.query.get(product_id)

    if request.method == "POST":
        cart = get_or_create(Cart, user_id=user_id)
        cart_item = get_or_create(CartItem, product=product, cart=cart)
        cart_item.increment()
        db.session.commit()

        return redirect(url_for('home', user_id=user_id))

    return render_nav('product.html', user_id, product=product)


@app.route('/<int:user_id>/basket', methods=["GET", "POST"])
def basket(user_id):
    if request.form:
        for key, value in request.form.items():
            item = CartItem.query.get(int(key))
            item.quantity = int(value)

            if item.quantity <= 0:
                db.session.delete(item)

        db.session.commit()

        return render_nav('home.html', user_id)

    items = db.session.query(CartItem).join(Cart).filter(
        Cart.user_id == user_id,
        Cart.active
    )

    return render_nav('basket.html', user_id, cart_items=items.all())



@app.route('/<int:user_id>/checkout', methods=["GET", "POST"])
def checkout(user_id):
    pass




if __name__ == "__main__":
    app.run(debug=True)