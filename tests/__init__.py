from flask_testing import TestCase
from app.models import *

from app import app, db


class TestBase(TestCase):
    def setUp(self) -> None:
        self.category = Category(name="Test Category")
        self.product = Product(name="Test Product", category=self.category, price=32, image="TestImage")
        self.cart = Cart(user_id=1)
        self.item = CartItem(product=self.product, cart=self.cart, quantity=2)

    def create_app(self):
        # Pass in testing configurations for the app.
        # Here we use sqlite without a persistent database for our tests.
        app.config.update(
              SQLALCHEMY_DATABASE_URI="sqlite:///test.db",
              SECRET_KEY='TEST_SECRET_KEY',
              DEBUG=True,
              WTF_CSRF_ENABLED=False
        )
        return app

    # Will be called after every test
    def tearDown(self):
        # Close the database session and remove all contents of the database
        db.session.remove()
        db.drop_all()