from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class LoginForm(FlaskForm):
    username = StringField("Username: ")
    login = SubmitField("Log In")


class OrderForm(FlaskForm):
    address_line_1 = StringField("Address")
    county = StringField("County")
    postcode = StringField("PostCode")
    number = StringField("Card Number")
    name = StringField("Owner full name")
    cvv = StringField("CVV")
    purchase = SubmitField("Place Order")


class PaymentForm(FlaskForm):
    number = StringField("Card Number")
    name = StringField("Owner full name")
    cvv = StringField("CVV")
    purchase = SubmitField("Place Order")