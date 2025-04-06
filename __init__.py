from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize extensions
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# Mongo from custom extensions file
from ingredient_converter.extensions import mongo

def create_app():
    app = Flask(__name__)

    # App configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
    app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/ingredient_converter')

    # Initialize extensions
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mongo.init_app(app)

    # Register blueprints
    from ingredient_converter.main import main
    from ingredient_converter.auth import auth
    from ingredient_converter.dashboard import dashboard
    from ingredient_converter.ml_service import ml

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(dashboard, url_prefix='/dashboard')
    app.register_blueprint(ml, url_prefix='/ml')  # change route to /ml/convert

    # User loader for Flask-Login
    from ingredient_converter.models import User
    from bson.objectid import ObjectId

    @login_manager.user_loader
    def load_user(user_id):
        try:
            user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            if user_data:
                return User(**user_data)
        except Exception as e:
            print(f"User load error: {e}")
        return None

    return app
