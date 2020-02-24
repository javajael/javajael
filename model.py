"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)


class Movie(db.Model):
    """Items - each item is a Movie with relevant information"""
    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_title = db.Column(db.String(64), nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    video_release_date = db.Column(db.DateTime, nullable=False)
    imdb_url = db.Column(db.String(64), nullable=False)
    # Should genre be a separate table with movie id as primary key (foreign key)
    # and each genre category is a column, with values of 0 or 1.  
    # 0 means it's not in that genre, 1 means it IS in that genre  pg 4/18 in lab
    # genre = 


class Rating(db.Model):
    """ Table containing a rating a particular user has given to a specific 
    movie
    """
    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
#     # is Timestamp necessary to the  objective - is it okay if it's null? 
#     # i.e. nullable could be False
#     time_stamp = db.Column(db.DateTime, nullable=True) 


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
