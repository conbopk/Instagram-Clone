from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.post import create_post, get_post, delete_post, like_post, get_user_posts


post_bp = Blueprint('post', __name__, url_prefix='/posts')

@post_bp.route('/', methods=['POST'])
@jwt_required()
def create_new_post():
    username = get_jwt_identity()
    data = request.get_json() or {}
    return create_post(username, data)

@post_bp.route('/<post_id>', methods=['GET'])
def get_single_post(post_id):
    return get_post(post_id)

@post_bp.route('/<post_id>', methods=['DELETE'])
@jwt_required()
def remove_post(post_id):
    username = get_jwt_identity()
    return delete_post(username, post_id)

@post_bp.route('/<post_id>/like', methods=['POST'])
@jwt_required()
def like_single_post(post_id):
    username = get_jwt_identity()
    return like_post(username, post_id)

@post_bp.route('/user/<username>', methods=['GET'])
def get_posts_by_user(username):
    return get_user_posts(username)





