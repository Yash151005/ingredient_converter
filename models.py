from flask_login import UserMixin
from bson import ObjectId
from ingredient_converter.extensions import mongo  # ✅ correct


class User(UserMixin):
    def __init__(self, _id, name, email, phone, gender, password):
        self.id = str(_id)
        self.name = name
        self.email = email
        self.phone = phone
        self.gender = gender
        self.password = password

    @staticmethod
    def get(user_id):
        user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return User(**user_data)
        return None

    @staticmethod
    def create_user(name, email, phone, gender, password):
        new_user = {
            "name": name,
            "email": email,
            "phone": phone,
            "gender": gender,
            "password": password
        }
        return mongo.db.users.insert_one(new_user).inserted_id

class ConversionHistory:
    @staticmethod
    def add_conversion(user_id, spoon_type, ingredient_type, quantity, result):
        mongo.db.conversions.insert_one({
            "user_id": ObjectId(user_id),
            "spoon_type": spoon_type,
            "ingredient_type": ingredient_type,
            "quantity": quantity,
            "result": result
        })

    @staticmethod
    def get_user_conversions(user_id):
        return list(mongo.db.conversions.find({"user_id": ObjectId(user_id)}))
