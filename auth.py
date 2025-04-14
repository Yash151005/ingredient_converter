from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import User
from extensions import mongo

import random
import string

auth = Blueprint("auth", __name__)

# Generate Captcha
def generate_captcha():
    captcha = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    session["captcha"] = captcha
    return captcha

# MongoDB connectivity check
def is_mongo_connected():
    try:
        mongo.db.command("ping")
        print("✅ MongoDB Connected")
        return True
    except Exception as e:
        print(f"❌ MongoDB is not initialized or reachable: {e}")
        return False

# ==================== LOGIN ====================
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        captcha = generate_captcha()
        return render_template("login.html", captcha=captcha)

    login_id = request.form.get("login_id")
    password = request.form.get("password")
    user_captcha = request.form.get("captcha")
    remember = bool(request.form.get("remember"))

    if session.get("captcha") != user_captcha:
        flash("Invalid captcha!", "error")
        return render_template("login.html", captcha=generate_captcha())

    if not is_mongo_connected():
        flash("Database connection error!", "error")
        return redirect(url_for("auth.login"))

    try:
        user_data = mongo.db.users.find_one(
            {"email": login_id} if "@" in login_id else {"phone": login_id}
        )
    except Exception as e:
        print(f"❌ MongoDB Query Error: {e}")
        flash("Database error occurred!", "error")
        return redirect(url_for("auth.login"))

    if not user_data or not check_password_hash(user_data["password"], password):
        flash("Invalid credentials!", "error")
        return render_template("login.html", captcha=generate_captcha())

    user = User(**user_data)
    login_user(user, remember=remember)
    return redirect(url_for("dashboard.dashboard_page"))

# ==================== SIGNUP ====================
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        captcha = generate_captcha()
        return render_template("signup.html", captcha=captcha)

    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    gender = request.form.get("gender")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    user_captcha = request.form.get("captcha")

    if session.get("captcha") != user_captcha:
        flash("Invalid captcha!", "error")
        return render_template("signup.html", captcha=generate_captcha())

    if password != confirm_password:
        flash("Passwords do not match!", "error")
        return render_template("signup.html", captcha=generate_captcha())

    if not is_mongo_connected():
        flash("Database connection error!", "error")
        return redirect(url_for("auth.signup"))

    try:
        if mongo.db.users.find_one({"email": email}):
            flash("Email already exists!", "error")
            return render_template("signup.html", captcha=generate_captcha())

        if mongo.db.users.find_one({"phone": phone}):
            flash("Phone number already exists!", "error")
            return render_template("signup.html", captcha=generate_captcha())

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        new_user = {
            "name": name,
            "email": email,
            "phone": phone,
            "gender": gender,
            "password": hashed_password,
        }

        user_id = mongo.db.users.insert_one(new_user).inserted_id

        if user_id:
            print(f"✅ User Created: {user_id}")
            flash("Account created successfully! Please login.", "success")
            return redirect(url_for("auth.login"))
        else:
            flash("Signup failed. Try again.", "error")
            return redirect(url_for("auth.signup"))

    except Exception as e:
        print(f"❌ MongoDB Insert Error: {e}")
        flash("An error occurred during signup.", "error")
        return redirect(url_for("auth.signup"))

# ==================== LOGOUT ====================
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
