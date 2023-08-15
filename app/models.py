from sqlalchemy_utils import ChoiceType

from app import db


DELIVERY_STATUS = [
    ("pending", 'Pending'),
    ("dispatched", 'Dispatched'),
    ("delivered", "Delivered")
]


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))
    carts = db.relationship('Cart', backref='user')
    orders = db.relationship('Order', backref='user')


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,  db.ForeignKey('user.id'), nullable=False)
    items = db.relationship('CartItem', backref='cart')

    @property
    def total(self):
        """Returns the total value of each item in the cart."""
        return sum(item.total for item in self.items)


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=0)
    cart_id = db.Column(db.Integer,  db.ForeignKey('cart.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    delivery_id = db.Column(db.Integer, db.ForeignKey('order.id'))

    @property
    def total(self):
        """Total value of CartItem accouting for quantity."""
        return self.quantity * self.product.price

    def increment(self):
        """Increments quantity."""
        self.quantity += 1
        db.session.commit()


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(ChoiceType(DELIVERY_STATUS), nullable=False)
    items = db.relationship('CartItem', backref='order')
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
