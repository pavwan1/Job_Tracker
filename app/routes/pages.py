from flask import Blueprint, request, jsonify, session, url_for
from ..models import db, User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect

pages = Blueprint('pages', __name__)

@pages.route('/')
def home():
    return redirect(url_for('pages.login'))

@pages.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    answer = data.get('security_answer')

    if not email or not password:
        return jsonify({"message": "Email, and password are required!"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(email=email, username=username, password=hashed_password, security_answer=answer)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

@pages.route('/login', methods=['POST', 'GET'])
def login():
    print("LOGIN API HIT")
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):   
        login_user(user)
        print(user)
        return jsonify({"message": "Login successful", "user": user.to_dict()}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@pages.route("/profile", methods=["GET"])
@login_required
def get_profile():
    user = current_user

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "username": user.username,
        "email": user.email,
        "skills": user.skills
    })

@pages.route("/profile", methods=["PUT"])
@login_required
def update_profile():
    user = current_user

    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    user.skills = data.get("skills", "")
    db.session.commit()

    return jsonify({"message": "Profile updated successfully"})

@pages.route('/logout', methods=['POST'])
@login_required
def logout():
    print("Logging out user:", current_user.is_authenticated)
    if current_user.is_authenticated:
        logout_user() 
        session.clear()
        return jsonify({"message": "Logout successful"}), 200
    else:
        return jsonify({"message": "No active session"}), 400
    
    
@pages.route("/forgot-password", methods=['Post'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    answer = data.get('answer')
    new_password = data.get('new_password')
    
    user = User.query.filter_by(email=email).first()
    
    if not user or user.security_answer.lower() != answer.lower():
        return jsonify({"message": "Invalid email or answer"}), 400
    
    user.password = generate_password_hash(new_password)
    db.session.commit()
    return jsonify({"message": "Password updated successfully"}), 200
    