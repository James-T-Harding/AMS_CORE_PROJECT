from app import app
from models import *

trees = Category(name="Trees")
shrubs = Category(name="Shrubs")

pear_tree = Product(
    name="Pear Tree",
    price=30,
    category=trees,
    image="pear.webp",
    description="A beautiful tree with delicious pears on its branches."
)
berry_bush = Product(
    name="Berry Bush",
    price=18,
    category=shrubs,
    image="berry-bush.jpg",
    description="A not particularly beautiful berry bush with non-edible berries on its branches."
)

user = User(username="John Buyer")


with app.app_context():
    db.drop_all()
    db.create_all()

    db.session.add_all([trees, shrubs, pear_tree, berry_bush, user])
    db.session.commit()