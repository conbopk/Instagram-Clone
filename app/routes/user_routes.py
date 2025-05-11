from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.user import get_profile, update_profile, update_profile_picture, get_all_users
from app.utils.helpers import api_response

user_bp = Blueprint('user', __name__, url_prefix='/users')


@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    username = get_jwt_identity()
    return get_profile(username)


@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_user_profile():
    username = get_jwt_identity()
    data = request.get_json() or {}
    return update_profile(username, data)


@user_bp.route('/profile/picture', methods=['POST'])
@jwt_required()
def update_user_picture():
    username = get_jwt_identity()
    picture_data = request.files.get('picture')
    if not picture_data:
        return api_response(message='No picture uploaded', status=400)
    return update_profile_picture(username, picture_data)


@user_bp.route('/<username>', methods=['GET'])
def get_user_profile(username):
    return get_profile(username)

@user_bp.route('/', methods=['GET'])
def list_users():
    return get_all_users()

