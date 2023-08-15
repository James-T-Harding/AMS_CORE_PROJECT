from app.create import populate_db
from tests import TestBase


class TestGetCartItems(TestBase):
    def setUp(self) -> None:
        populate_db()