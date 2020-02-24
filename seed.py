"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User
from model import Rating
from model import Movie

from model import connect_to_db, db
from server import app

from datetime import datetime


def load_users(user_filename):
    """Load users from u.user into database."""

    print("Users")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open(user_filename):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies(movie_filename):
    """Load movies from u.item into database."""
    print("Movies")

    for i, row in enumerate(open(movie_filename)):
        row = row.rstrip()
        # release date is in brackets in the movie title - will have to split
        # out after

        # List slicing would be a better way to assign these variables
        # (movie_id, movie_title, date_str, video_release_date, imdb_url,
        #     unknown, action, adventure, animation, children, comedy, crime,
        #     documentary, drama, fantasy, film_noir, horror, musical, mystery,
        #     romance, sci_fi, thriller, war, western) = row.split("|")

        # Use List slicing to drop the last part of the line - it's genre info
        # and we won't be needing it.
        (movie_id, movie_title, date_str, video_release_date,
            imdb_url) = row.split("|")[:5]

        # Figure out how to Remove the  release date from the movie title.
        # Its in the parentheses at the end of the movie title.     
        format = "%d-%b-%Y"
        release_date = datetime.strptime(date_str, format)
        print(f"date_str = {date_str}, release_date = {release_date}")

        # The release date is actually at the end of the title string in
        # brackets. So we need to strip that out to get only the title.
        # so take off the last 7 chars since (YYYY) == 7
        movie_title = movie_title[:-7]

        print("Movie title is : ", movie_title)
        print("IMDB URL: ", imdb_url)

        movie = Movie(movie_id=movie_id,
                      movie_title=movie_title,
                      release_date=release_date,
                      imdb_url=imdb_url
                      )

        # We need to add to the session or it won't ever be stored
        db.session.add(movie)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)

    # Once we're done, we should commit our work
    db.session.commit()


def load_ratings(rating_filename):
    """Load ratings from u.data into database."""
    print("Ratings")

    for i, row in enumerate(open(rating_filename)):
        row = row.rstrip()

        user_id, movie_id, score, timestamp = row.split("\t")
        rating = Rating(user_id=user_id,
                        movie_id=movie_id,
                        score=score)

        # We need to add to the session or it won't ever be stored
        db.session.add(rating)
        # provide some sense of progress
        if i % 1000 == 0:
            print(i)

            # An optimization: if we commit after every add, the database
            # will do a lot of work committing each record. However, if we
            # wait until the end, on computers with smaller amounts of
            # memory, it might thrash around. By committing every 1,000th
            # add, we'll strike a good balance.

            db.session.commit()

    # Once we're done, we should commit our work
    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    user_filename = "seed_data/u.user"
    movie_filename = "seed_data/u.item"
    rating_filename = "seed_data/u.data"

    load_users(user_filename)
    load_movies(movie_filename)
    load_ratings(rating_filename)
    set_val_user_id()
