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
    address_line_1 = db.Column(db.String(50))
    county = db.Column(db.String(30))
    postcode = db.Column(db.String(10))
    carts = db.relationship('Cart', backref='user')


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment = db.Column(db.Integer)
    user_id = db.Column(db.Integer,  db.ForeignKey('user.id'), nullable=False)
    items = db.relationship('CartItem', backref='cart')

    @property
    def total(self):
        return sum(item.total for item in self.items)

    def place_order(self):
        self.payment = self.total

        db.session.add(Order(items=self.items, status="pending"))
        db.session.commit()


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=0)
    cart_id = db.Column(db.Integer,  db.ForeignKey('cart.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    delivery_id = db.Column(db.Integer, db.ForeignKey('order.id'))

    @property
    def total(self):
        return self.quantity * self.product.price

    def increment(self):
        self.quantity += 1
        db.session.commit()


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(ChoiceType(DELIVERY_STATUS), nullable=False)
    items = db.relationship('CartItem', backref='order')


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