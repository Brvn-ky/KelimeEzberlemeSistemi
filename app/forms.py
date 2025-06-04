from flask_wtf import FlaskForm 
from wtforms.validators import DataRequired, Length
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed


class RegisterForm(FlaskForm):
    username = StringField('Kullanici Adi', validators=[DataRequired(), Length(min=4, max=150)])
    password = PasswordField('Sifre', validators=[DataRequired()])
    submit = SubmitField('Kayit Ol')

class LoginForm(FlaskForm):
    username = StringField('Kullanici Adi', validators=[DataRequired()])
    password = PasswordField('Sifre', validators=[DataRequired()])
    submit = SubmitField('Giris Yap')

class ResetPasswordForm(FlaskForm):
    username = StringField('Kullanici Adi', validators=[DataRequired()])
    new_password = PasswordField('Yeni sifre', validators=[DataRequired()])
    submit = SubmitField('Sifreyi Sifirla')


class WordForm(FlaskForm):
    eng_word = StringField('Ingilizce Kelime', validators=[DataRequired()])
    tur_word = StringField('Turkce Karsiligi', validators=[DataRequired()])
    sentence = StringField('Ornek Cumle', validators=[DataRequired()])
    image = FileField('Resim Yukle', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Kelimeyi Ekle')

class QuizForm(FlaskForm):
    answer = StringField('Turkce Karsiligi', validators=[DataRequired()])
    submit = SubmitField('Cevapla')

class SettingsForm(FlaskForm):
    quiz_limit = IntegerField('Quizte G0sterilecek Kelime Sayisi', validators=[
        DataRequired(), NumberRange(min=1, max=20)
    ])
    submit = SubmitField('Ayarlari Kaydet')
