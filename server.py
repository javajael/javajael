"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)

from model import User, Rating, Movie, connect_to_db, db
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show list of all users"""
    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/registration')
def registration():
    """ Register a new user """
    return render_template("registration.html")


@app.route('/create_user')
def create_user():
    """ checks database to see if a user exists and if not creates the
    entry in the database. """
    email = request.args.get('email')
    password = request.args.get('password')

    # check db to see if the email exists in the db
    user = User.query.filter_by(email=email).all()
    if user is not None:
        return render_template("login.html")
    else:
        # take the email and password and add it to the entry in the db.
        user = User(email=email, password=password)
        # insert a row into the table for this user
        # if the user was created successfully flash message


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
