from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms import RegisterForm, LoginForm , ResetPasswordForm
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

        if user is None:
            flash('Kullanici bulunamadi. Lutfen kayit olun.', 'danger')
            return redirect(url_for('main.register'))

        if not bcrypt.check_password_hash(user.password, form.password.data):
            flash('Sifre hatali, tekrar deneyin.', 'danger')
            return redirect(url_for('main.login'))

        # Giriþ baþarýlý
        login_user(user)
        flash('Giris basarili!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('login.html', form=form)



@main.route('/dashboard')
@login_required
def dashboard():
    return "Hos geldin!"

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            hashed_pw = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            user.password = hashed_pw
            db.session.commit()
            flash('Sifre basariyla guncellendi.', 'success')
            return redirect(url_for('main.login'))
        else:
            flash('Kullanici bulunamadi.', 'danger')
    return render_template('reset_password.html', form=form)
