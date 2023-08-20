from tests import TestBase

from app.routes import get_cart_items, get_or_create

class TestFunctions(TestBase):
    def test_get_cart_items(self):
        self.cart