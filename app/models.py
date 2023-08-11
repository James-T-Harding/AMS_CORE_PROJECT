from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    carts = db.relationship('Cart', backref='user')


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer,  db.ForeignKey('user.id'), nullable=False)
    items = db.relationship('CartItem', backref='cart')


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=0)
    cart_id = db.Column(db.Integer,  db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def increment(self):
        self.quantity += 1
        db.session.commit()


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