from pymongo import MongoClient

def get_db():
    try:
        client = MongoClient("mongodb://localhost:27017")
        db = client["ingredient_converter"]
        print("✅ MongoDB Connected Successfully!")
        return db
    except Exception as e:
        print(f"❌ MongoDB Connection Error: {e}")
        return None
