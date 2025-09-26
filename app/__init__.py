from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from .config import Config

# Initialisation des extensions
db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialisation des extensions avec l'app
    db.init_app(app)
    csrf.init_app(app)
    
    # Import des modèles après l'initialisation de db
    from . import models
    
    # Import des blueprints
    from .auth.routes import auth_bp
    from .train.routes import train_bp
    from .reservation.routes import reservation_bp
    from .main.routes import main_bp
    
    # Enregistrement des blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(train_bp, url_prefix='/train')
    app.register_blueprint(reservation_bp, url_prefix='/reservation')
    
    # Création des tables
    with app.app_context():
        db.create_all()
    
    return app