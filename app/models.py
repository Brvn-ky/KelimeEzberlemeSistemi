from app import db
from flask_login import UserMixin
from app.extensions import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eng_word = db.Column(db.String(100), nullable=False)
    tur_word = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200), nullable=True)  # resim dosya yolu

    samples = db.relationship('WordSample', backref='word', lazy=True)

class WordSample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), nullable=False)
    sentence = db.Column(db.Text, nullable=False)
