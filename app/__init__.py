# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Crear una instancia global de SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies_reviews.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar base de datos con la app
    db.init_app(app)

    # Importar y registrar los blueprints (rutas)
    from .routes import main
    app.register_blueprint(main)

    return app
