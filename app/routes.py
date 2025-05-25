from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms import RegisterForm, LoginForm
from app.models import User
from app import db, bcrypt
from flask_login import login_user, logout_user, login_required
# -*- coding: <meta charset="UTF-8"> -*-
from app.extensions import db

main = Blueprint('main', __name__)

@main.route('/register', methods=['GET', 'POST'])

def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Kayit basarili!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Hatali kullanici adi veya sifre.', 'danger')
    return render_template('login.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    return "Hos geldin!"

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))
