import os
from datetime import timedelta, datetime
from email_validator import validate_email, EmailNotValidError

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
)
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Expiration time for tokens
access_minutes = int(os.getenv('ACCESS_TOKEN_EXPIRES', 15))
refresh_days = int(os.getenv('REFRESH_TOKEN_EXPIRES', 7))
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret')

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=access_minutes)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=refresh_days)

# Importar db y User después de configurar la app
from models import db, User

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager()
jwt.init_app(app)

with app.app_context():
    db.create_all()

#Validaciones
def _normalize_username(username: str) -> str:
    try:
        valid = validate_email(username, check_deliverability=False)
        return valid.email
    except EmailNotValidError as e:
        return ValueError(str(e))
    
def _require_json(keys):
    data = request.get_json()
    missing = [key for key in keys if key not in data or data[key] in [None, '']]
    if missing:
        return jsonify({"error": f"Missing or empty fields: {', '.join(missing)}"}), 400
    return data, None

# Routes
@app.post('/auth/register')
def register():
    data, error = _require_json(['email', 'password'])
    if error:
        return error

    try:
        email = _normalize_username(data['email'])
    except ValueError as e:
        return jsonify({"error": f"Invalid email address: {str(e)}"}), 400
    
    password = data['password']
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters long"}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400
    
    user = User(username=data['email'], email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=user.id, additional_claims={"username": user.email})
    refresh_token = create_refresh_token(identity=user.id)
    return jsonify({
        "message": "User registered successfully",
        "user": user.to_dict(),
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 201
    

@app.post('/auth/login')
def login():
    data, error = _require_json(['email', 'password'])
    if error:
        return error

    try:
        email = _normalize_username(data['email'])
    except ValueError as e:
        return jsonify({"error": f"Invalid email address: {str(e)}"}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Invalid email or password"}), 401
    
    access_token = create_access_token(identity=user.id, additional_claims={"username": user.email})
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        "message": "Login successful",
        "user": user.to_dict(),
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200


@app.post('/auth/refresh')
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    new_access_token = create_access_token(identity=user.id, additional_claims={"username": user.email})
    
    return jsonify({
        "access_token": new_access_token
    }), 200


@app.get('/auth/me')
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({
        "user": user.to_dict()
    }), 200


# Error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Token has expired"}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"error": "Invalid token"}), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"error": "Authorization token required"}), 401
    

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', 'true').lower() in ['true', '1', 't'])
