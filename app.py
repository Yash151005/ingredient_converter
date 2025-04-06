# app.py
from flask import Flask
from flask_login import LoginManager
from extensions import mongo
from config import Config
from models import User
from bson.objectid import ObjectId

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    mongo.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Blueprints
    from auth import auth as auth_blueprint
    from main import main as main_blueprint
    from dashboard import dashboard as dashboard_blueprint
    from ml_service import ml as ml_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(main_blueprint)
    app.register_blueprint(dashboard_blueprint, url_prefix="/dashboard")
    app.register_blueprint(ml_blueprint)

    return app

@login_manager.user_loader
def load_user(user_id):
    try:
        user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return User(**user_data)
    except Exception as e:
        print(f"Error loading user: {e}")
    return None
