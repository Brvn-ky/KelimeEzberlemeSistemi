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
from app.forms import SettingsForm
from app.forms import RegisterForm, LoginForm, ResetPasswordForm, WordForm, QuizForm, SettingsForm
from datetime import datetime, timedelta

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

        # Giriş başarılı
        login_user(user)
        flash('Giris basarili!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('login.html', form=form)




@main.route('/dashboard')
@login_required
def dashboard():
    stats = QuizHistory.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', stats=stats)



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

    processed = []
    for record in stats:
        total_attempts = record.correct_count + record.wrong_count
        if total_attempts == 0:
            percentage = "-"
        else:
            percentage = f"%{(record.correct_count / total_attempts) * 100:.0f}"

        processed.append({
            "kelime": record.word.eng_word,
            "correct": record.correct_count,
            "wrong": record.wrong_count,
            "last": record.last_answered.strftime('%d.%m.%Y %H:%M') if record.last_answered else "-",
            "status": "✅" if record.correct_count >= 6 else "⏳",
            "success": percentage
        })

    return render_template("progress.html", stats=processed)

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

    # Kullanıcı ayarına göre sınırla
    quiz_list = quiz_list[:current_user.quiz_limit]

    if not quiz_list:
        flash("📅 Bugün çalışman gereken kelime yok. Tebrikler!", "info")
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
            flash(f"✅ Doğru! Seviye: {history.level}", "success")
        else:
            history.correct_count = 0
            history.wrong_count += 1
            history.level = 0
            flash("❌ Yanlış! Seviye sıfırlandı.", "danger")

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
            "durum": "✔️ Gösterilmeli" if gecmis else "⏳ Henüz değil",
            "ilerleme": progress
        })

    return render_template("history.html", logs=word_logs)


import matplotlib.pyplot as plt
import io
import base64

@main.route('/chart')
@login_required
def chart():
    records = QuizHistory.query.filter_by(user_id=current_user.id).all()

    labels = [r.word.eng_word for r in records]
    corrects = [r.correct_count for r in records]
    wrongs = [r.wrong_count for r in records]
    levels = [r.level for r in records]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(labels, corrects, label="Doğru", color='green')
    ax.bar(labels, wrongs, bottom=corrects, label="Yanlış", color='red')
    ax.set_title("Kelimelere Göre Cevap Sayıları")
    ax.set_ylabel("Cevap Sayısı")
    ax.legend()
    plt.xticks(rotation=45)

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img = base64.b64encode(buf.getvalue()).decode()

    return render_template('chart.html', img_data=img)


import csv
from flask import Response

@main.route('/export')
@login_required
def export():
    records = QuizHistory.query.filter_by(user_id=current_user.id).all()

    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(["Kelime", "Doğru", "Yanlış", "Seviye", "Son Cevap"])

    for r in records:
        cw.writerow([
            r.word.eng_word,
            r.correct_count,
            r.wrong_count,
            r.level,
            r.last_answered.strftime("%d.%m.%Y %H:%M") if r.last_answered else "-"
        ])

    output = Response(si.getvalue(), mimetype='text/csv')
    output.headers["Content-Disposition"] = "attachment; filename=gecmis.csv"
    return output

@main.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        current_user.quiz_limit = form.quiz_limit.data
        db.session.commit()
        flash("Ayarlar başarıyla güncellendi!", "success")
        return redirect(url_for('main.dashboard'))

    form.quiz_limit.data = current_user.quiz_limit
    return render_template('settings.html', form=form)

import pdfkit
from flask import make_response, render_template

import pdfkit
import matplotlib.pyplot as plt
import io
import base64
from flask import make_response, render_template
from datetime import datetime

@main.route("/report/pdf")
@login_required
def download_report():
    stats = QuizHistory.query.filter_by(user_id=current_user.id).all()

    # 1. Grafik çiz
    labels = [r.word.eng_word for r in stats]
    corrects = [r.correct_count for r in stats]
    wrongs = [r.wrong_count for r in stats]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(labels, corrects, label="Doğru", color='green')
    ax.bar(labels, wrongs, bottom=corrects, label="Yanlış", color='red')
    ax.set_title("Kelimelere Göre Cevap Sayıları")
    ax.set_ylabel("Cevap")
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    graph_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    # 2. HTML render
    rendered = render_template("report_template.html", stats=stats, chart=graph_base64)

    # 3. PDF'e dönüştür
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")  # senin yolun buysa
    pdf = pdfkit.from_string(rendered, False, configuration=config)

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"inline; filename=rapor_{datetime.now().strftime('%Y%m%d')}.pdf"
    return response




