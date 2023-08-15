from app import app, bcrypt
from models import *

trees = Category(name="Trees")
shrubs = Category(name="Shrubs")
indoors = Category(name="Indoors")

pear_tree = Product(
    name="Pear Tree",
    price=30,
    category=trees,
    image="pear.webp",
    description="A beautiful tree with delicious pears on its branches."
)
pine_tree = Product(
    name="Pine Tree",
    price=40,
    category=trees,
    image="pine.webp",
    description="An evergreen, coniferous tree of varied size. Commonly used as a Christmas ornament."
)
flowers = Product(
    name="Flower pot.",
    price=15,
    category=indoors,
    image="flowers.jpg",
    description="A pot to store flowers."
)


berry_bush = Product(
    name="Berry Bush",
    price=18,
    category=shrubs,
    image="berry-bush.jpg",
    description="A not particularly beautiful berry bush with non-edible berries on its branches."
)

user = User(username="John Buyer", password=bcrypt.generate_password_hash("password"))


def populate_db():
    with app.app_context():
        db.drop_all()
        db.create_all()

        db.session.add_all([trees, shrubs, flowers, user])
        db.session.commit()


if __name__ == "__main__":
    populate_db()
