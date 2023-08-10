from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class LoginForm(FlaskForm):
    username = StringField("Username: ")
    login = SubmitField("Log In")


class AddBasketForm(FlaskForm):
    add = SubmitField("Add")