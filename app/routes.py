from app import app, bcrypt
from app.models import *
from app.forms import *

from flask import redirect, url_for, render_template, request


def get_cart_items(user_id):
    """
    Gets all items of all carts associated with the passed in user.
    """
    items = db.session.query(CartItem).join(Cart).filter(
        Cart.user_id == user_id,
    )
    return items.all()


def render_nav(template, user_id, **kwargs):
    """
    Returns a template with useful keyword context already populated. Necessary for rendering any template
    that inherits from base.html.
    """

    kwargs.update(user_id=user_id)
    kwargs["home_url"] = url_for('home', user_id=user_id)
    kwargs["products_url"] = url_for('products', user_id=user_id)
    kwargs["basket_url"] = url_for('basket', user_id=user_id)
    kwargs["cart_items"] = get_cart_items(user_id)
    kwargs["cart_total"] = sum(item.total for item in kwargs["cart_items"])
    kwargs["style_url"] = url_for('static', filename='style.css')

    return render_template(template, **kwargs)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.data.get("username")
        user = User.query.filter_by(username=username).first()
        password = form.data.get("password")

        if bcrypt.check_password_hash(user.password, password):
            return redirect(url_for('home', user_id=user.id))

    return render_template('login.html', form=form)


@app.route('/<int:user_id>/home')
def home(user_id):
    return render_nav('home.html', user_id, categories=Category.query.all())


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
        cart.add_item(product)

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
        return redirect(url_for('checkout', user_id=user_id))

    return render_nav('basket.html', user_id)


@app.route('/<int:user_id>/checkout', methods=["GET", "POST"])
def checkout(user_id):
    form = OrderForm()

    if form.validate_on_submit():
        cart = Cart.query.filter_by(user_id=user_id).first()

        order = Delivery(
            address_line_1=form.data.get("address_line_1"),
            county=form.data.get("county"),
            postcode=form.data.get("postcode"),
            user_id=user_id,
            status="pending",
            payment=cart.total,
            items=cart.items,
        )

        db.session.add(order)
        db.session.delete(cart)
        db.session.commit()

        return redirect(url_for('home', user_id=user_id))

    return render_nav('checkout.html', user_id, form=form)


if __name__ == "__main__":
    app.run(debug=True)