from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.post import create_post, get_post, delete_post, like_post, get_user_posts, unlike_post, get_post_likes, get_news_feed
from app.models.user import User


post_bp = Blueprint('post', __name__, url_prefix='/api/posts')

@post_bp.route('/', methods=['POST'])
@jwt_required()
def create_new_post():
    current_user_id = get_jwt_identity()
    current_user = User.query.filter_by(current_user_id)
    return create_post(current_user)


@post_bp.route('/<int:post_id>', methods=['GET'])
@jwt_required()
def get_single_post(post_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    return get_post(current_user, post_id)


@post_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def remove_post(post_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    return delete_post(current_user, post_id)


@post_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def view_user_posts(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    return get_user_posts(current_user, user_id)


@post_bp.route('/<int:post_id>/like', methods=['POST'])
@jwt_required()
def like_single_post(post_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    return like_post(current_user, post_id)


@post_bp.route('/<int:post_id>/unlike', methods=['DELETE'])
@jwt_required()
def unlike_single_post(post_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    return unlike_post(current_user, post_id)


@post_bp.route('/<int:post_id>/likes', methods=['GET'])
@jwt_required()
def view_post_likes(post_id):
    return get_post_likes(post_id)


@post_bp.route('/feed', methods=['GET'])
@jwt_required()
def view_news_feed():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    return get_news_feed(current_user)




