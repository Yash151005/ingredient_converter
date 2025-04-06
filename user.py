from flask_login import UserMixin
from ingredient_converter import login_manager, db, bcrypt
from bson.objectid import ObjectId
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    user_data = db.users.find_one({'_id': ObjectId(user_id)})
    if user_data:
        return User(user_data)
    return None

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.name = user_data['name']
        self.email = user_data['email']
        self.phone = user_data['phone']
        self.gender = user_data['gender']
        self.password_hash = user_data['password']
        
    def get_id(self):
        return self.id
    
    @staticmethod
    def create_user(name, email, phone, gender, password):
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user_id = db.users.insert_one({
            'name': name,
            'email': email,
            'phone': phone,
            'gender': gender,
            'password': password_hash,
            'created_at': datetime.now()
        }).inserted_id
        
        user_data = db.users.find_one({'_id': user_id})
        return User(user_data)
    
    @staticmethod
    def authenticate(login, password):
        # Check if login is email or phone
        if '@' in login:
            user_data = db.users.find_one({'email': login})
        else:
            user_data = db.users.find_one({'phone': login})
            
        if user_data and bcrypt.check_password_hash(user_data['password'], password):
            return User(user_data)
        return None