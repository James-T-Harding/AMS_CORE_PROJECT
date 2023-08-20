from app.models import *
from tests import TestBase


class TestModels(TestBase):
    def test_item_total(self):
        self.assertEqual(64, self.item.total)

    def test_increment(self):
        self.item.increment()
        self.assertEqual(3, self.item.quantity)

    def test_cart_total(self):
        product = Product(name="Other Product", category=self.category, price=24, image="TestImage")
        CartItem(product=product, cart=self.cart, quantity=1)

        self.assertEqual(88, self.cart.total)

    def test_category_image(self):
        self.assertEqual(self.category.image, "TestImage")