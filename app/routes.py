from app import app
from app.models import User
from forms import *

from flask import redirect, url_for, render_template


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.data.get("username")
        user = User.query.filter_by(username=username).first()

        return redirect(url_for('home', user_id=user.id))

    return render_template('login.html', form=form)


@app.route('/<int:user_id>')
def home(user_id):
    return render_template('home.html', user_id=user_id)


if __name__ == "__main__":
    app.run(debug=True)