
from app.models import User
from app import db, bcrypt
# -*- coding: <meta charset="UTF-8"> -*-
from app.extensions import db
import os
from flask import current_app
from werkzeug.utils import secure_filename
from app.models import Word, WordSample
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import RegisterForm, LoginForm, ResetPasswordForm, WordForm
from app.models import User, Word, WordSample
from app.extensions import db, bcrypt
from flask_login import login_user, logout_user, login_required, current_user
from app.models import QuizHistory
from datetime import datetime
import random
from app.forms import QuizForm
from app.models import QuizHistory
from flask_login import current_user

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
    stats = QuizHistory.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', stats=stats)

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


@main.route('/add_word', methods=['GET', 'POST'])
def add_word():
    form = WordForm()

    if form.validate_on_submit():
        filename = None
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            image_path = os.path.join('app/static/uploads', filename)
            form.image.data.save(image_path)

        word = Word(eng_word=form.eng_word.data, tur_word=form.tur_word.data, image=filename)
        db.session.add(word)
        db.session.commit()

        sample = WordSample(word_id=word.id, sentence=form.sentence.data)
        db.session.add(sample)
        db.session.commit()

        flash('Kelime basariyla eklendi.', 'success')
        return redirect(url_for('main.add_word'))

    return render_template('add_word.html', form=form)


@main.route('/progress')
@login_required
def progress():
    stats = QuizHistory.query.filter_by(user_id=current_user.id).all()
    return render_template('progress.html', stats=stats)

from datetime import datetime, timedelta

def is_due(history):
    if not history.last_answered:
        return True

    now = datetime.utcnow()
    delay_map = {
        0: timedelta(seconds=0),
        1: timedelta(days=1),
        2: timedelta(days=3),
        3: timedelta(weeks=1),
        4: timedelta(days=30),
        5: timedelta(days=90),
        6: timedelta(days=9999),  # öðrenilmiþ
    }

    next_due = history.last_answered + delay_map.get(history.level, timedelta(days=9999))
    return now >= next_due

@main.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    form = QuizForm()
    all_words = Word.query.all()

    # uygun kelimeleri filtrele
    quiz_list = []
    for word in all_words:
        history = QuizHistory.query.filter_by(user_id=current_user.id, word_id=word.id).first()
        if not history or is_due(history):
            quiz_list.append(word)

    if not quiz_list:
        flash("?? Bugün çalýþman gereken kelime yok. Tebrikler!", "info")
        return redirect(url_for('main.dashboard'))

    word = random.choice(quiz_list)

    if form.validate_on_submit():
        user_answer = form.answer.data.strip().lower()
        correct_answer = word.tur_word.lower()
        is_correct = (user_answer == correct_answer)

        history = QuizHistory.query.filter_by(user_id=current_user.id, word_id=word.id).first()
        if not history:
            history = QuizHistory(user_id=current_user.id, word_id=word.id, correct_count=0, wrong_count=0, level=0)

        if is_correct:
            history.correct_count += 1
            history.level = min(history.level + 1, 6)
            flash(f"? Doðru! Seviye: {history.level}", "success")
        else:
            history.correct_count = 0
            history.wrong_count += 1
            history.level = 0
            flash("? Yanlýþ! Seviye sýfýrlandý.", "danger")

        history.last_answered = datetime.utcnow()
        db.session.add(history)
        db.session.commit()
        return redirect(url_for('main.quiz'))

    return render_template('quiz.html', form=form, word=word)

@main.route('/history')
@login_required
def history():
    records = QuizHistory.query.filter_by(user_id=current_user.id).all()

    delay_map = {
        0: timedelta(seconds=0),
        1: timedelta(days=1),
        2: timedelta(days=3),
        3: timedelta(weeks=1),
        4: timedelta(days=30),
        5: timedelta(days=90),
        6: timedelta(days=9999),
    }

    word_logs = []

    now = datetime.utcnow()

    for r in records:
        kelime = r.word.eng_word
        level = r.level
        last = r.last_answered or datetime(1970,1,1)
        expected = last + delay_map.get(level, timedelta(days=9999))
        gecmis = now >= expected
        progress = f"%{(level/6)*100:.0f}"

        word_logs.append({
            "kelime": kelime,
            "level": level,
            "last": last.strftime("%d.%m.%Y %H:%M"),
            "bekleme": delay_map.get(level).days if level < 6 else "-",
            "durum": "?? Gösterilmeli" if gecmis else "? Henüz deðil",
            "ilerleme": progress
        })

    return render_template("history.html", logs=word_logs)
