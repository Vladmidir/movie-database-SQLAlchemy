import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


# absolute path of the base (this) directory
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# specify the database to connect to. Stick to sqlite for now.
# figure out how to connect MySql in the future (look at the previous project)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'database.db')
# Disable tracking to save memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


# int being a converter
@app.route('/<int:movie_id>/')
def movie(movie_id):
    # returns 404 instead of None when not found
    movie = Movie.query.get_or_404(movie_id)
    return render_template('movie.html', movie=movie)


@app.route('/create/', methods=['GET', 'POST'])
def create():
    # what about escaping inputs?
    if request.method == 'POST':
        return add_movie(request.form)
    else:
        return render_template('create.html')


@app.route('/<int:movie_id>/edit/', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        return edit_movie(request.form, movie)
    else:
        return render_template('edit.html', movie=movie)


@app.post('/<int:movie_id>/delete/')
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('index'))


def add_movie(form):
    name = form['name']
    description = form['description']
    rating = int(form['rating']) # is the conversion necessary?

    movie = Movie(name=name, description=description, rating=rating)

    db.session.add(movie)
    db.session.commit()

    return redirect(url_for('index'))


def edit_movie(form, movie):
    movie.name = form['name']
    movie.description = form['description']
    movie.rating = form['rating']
    # since the id is unique, this overrides the existing entry
    db.session.add(movie)
    db.session.commit()

    return redirect(url_for('index'))


# create a model for the table
class Movie(db.Model):
    """
    Represents table of Movies in the database.
    Do I need to make the initializer? Show I use proper assignment?
    self.value = value?
    Maybe not, because it inherits.
    """
    # First argument is column type.
    # Followups are column configurations.
    # every table requires a primary key
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    # how to I add decimals for rating? How to I set max and min values?
    # (those being representation invariants)
    rating = db.Column(db.Integer)
    # Change this to released at and record movie release date.
    added_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        """String representation"""
        return f'Movie {self.name}'

