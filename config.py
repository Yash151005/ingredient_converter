# ingredient_converter/config.py
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "ghdyolfDOYVUSHdvLD")
    MONGO_URI = "mongodb://localhost:27017/ingredient_converter"
