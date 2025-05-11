from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    movies = db.relationship('Movie', backref='user', lazy=True, cascade='all, delete-orphan')

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150))
    release_year = db.Column(db.String(10))
    genre = db.Column(db.String(100))
    director = db.Column(db.String(100))
    rating = db.Column(db.String(10))
    poster_url = db.Column(db.String(300))
    plot = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))