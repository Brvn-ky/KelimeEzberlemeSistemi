from flask import Flask
from app.extensions import db, bcrypt, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes import main
    app.register_blueprint(main)

    return app
