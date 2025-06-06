import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'cokguclubirsey'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'kelimeler.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
