from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.user import get_profile, update_profile, get_user_profile
from app.models.user import User

user_bp = Blueprint('user', __name__, url_prefix='/users')


@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    return get_profile(current_user)


@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_user_profile():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    data = request.get_json() or {}

    return update_profile(current_user, data)


@user_bp.route('/<int:user_id>/profile', methods=['GET'])
@jwt_required()
def view_other_profile(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    return get_user_profile(current_user, user_id)


# @user_bp.route('/', methods=['GET'])
# def list_users():
#     return get_all_users()

