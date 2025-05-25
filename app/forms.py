from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class RegisterForm(FlaskForm):
    username = StringField('Kullanici Adi', validators=[DataRequired(), Length(min=4, max=150)])
    password = PasswordField('Sifre', validators=[DataRequired()])
    submit = SubmitField('Kayit Ol')

class LoginForm(FlaskForm):
    username = StringField('Kullanici Adi', validators=[DataRequired()])
    password = PasswordField('Sifre', validators=[DataRequired()])
    submit = SubmitField('Giris Yap')
