from app import db


def get_or_create(model, **kwargs):
    """
    Either gets the first instance of a model associated with keyword filters, or creates a new one
    and returns that if none are available.
    """
    if result := model.query.filter_by(**kwargs).first():
        return result

    item = model(**kwargs)
    db.session.add(item)
    db.session.commit()

    return item


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(120))
    carts = db.relationship('Cart', backref='user')
    orders = db.relationship('Delivery', backref='user')


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,  db.ForeignKey('user.id'), nullable=False)
    items = db.relationship('CartItem', backref='cart')

    @property
    def total(self):
        """Returns the total value of each item in the cart."""
        return sum(item.total for item in self.items)

    def __contains__(self, product):
        return any(item.product == product for item in self.items)

    def add_item(self, product, quantity=1):
        """Adds a given product to the cart, with an option to adjust the quantity (defaults to 1)"""
        item = get_or_create(CartItem, cart=self, product=product)
        item.quantity += quantity
        db.session.commit()


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=0)
    cart_id = db.Column(db.Integer,  db.ForeignKey('cart.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    delivery_id = db.Column(db.Integer, db.ForeignKey('delivery.id'))

    @property
    def total(self):
        """Total value of CartItem accouting for quantity."""
        return self.quantity * self.product.price


class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(30))
    items = db.relationship('CartItem', backref='delivery')
    address_line_1 = db.Column(db.String(50))
    county = db.Column(db.String(30))
    postcode = db.Column(db.String(10))
    payment = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(30))
    price = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    items = db.relationship('CartItem', backref='product')


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    products = db.relationship('Product', backref='category')

    @property
    def image(self):
        """Returns image url of first product associated with the category, if there are any."""
        return self.products[0].image if self.products else ""
