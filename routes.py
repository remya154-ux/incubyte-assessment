from flask import Flask, request, jsonify
from models import db
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # CRUD endpoints
    # Create employee
    # Read all employees
    # Read one employee details
    # Update employee details
    # Delete

    return app