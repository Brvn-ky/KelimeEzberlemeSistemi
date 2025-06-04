from app import db
from flask_login import UserMixin
from app.extensions import db
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    quiz_limit = db.Column(db.Integer, default=1)  # varsayılan: 1 kelime


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

from datetime import datetime

class QuizHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), nullable=False)
    correct_count = db.Column(db.Integer, default=0)
    wrong_count = db.Column(db.Integer, default=0)
    last_answered = db.Column(db.DateTime)
    level = db.Column(db.Integer, default=0)

    word = db.relationship("Word", backref="histories")

class SettingsForm(FlaskForm):
    quiz_limit = IntegerField('Quizte Gosterilecek Kelime Sayisi', validators=[DataRequired(), NumberRange(min=1, max=20)])
    submit = SubmitField('Ayarları Kaydet')
