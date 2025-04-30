from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'  # Redirigir a esta vista si no está autenticado

@login_manager.user_loader
def load_user(user_id):
    from app.models import Usuario
    return Usuario.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.secret_key = 'e5b0c3f8a9d4e7f1b2c3d4e5f6a7b8c9'
    login_manager.init_app(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies_reviews.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True  # Habilitar el modo de depuración

    db.init_app(app)
    migrate = Migrate(app, db)

    from .routes import main
    app.register_blueprint(main)

    return app

