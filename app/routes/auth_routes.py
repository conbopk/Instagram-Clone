from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app.controllers.auth import register_user, login_user, logout_user, get_current_user
from app.utils.helpers import api_response
from app.models.user import User


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


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)

    return api_response(
        data={
            'access_token': access_token
        }
    )


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    return get_current_user(current_user)


