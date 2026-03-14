from config import Config
from flask import Flask
from .models import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    from . import routes
    routes.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app