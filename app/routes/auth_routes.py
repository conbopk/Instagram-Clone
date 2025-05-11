from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.controllers.auth import register_user, login_user, logout_user


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    return register_user(data)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    return login_user(data)

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return logout_user()



