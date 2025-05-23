from app.models.user import User
from app.utils.helpers import api_response
from flask import request
from app.utils.storage import upload_file_to_gcs, delete_file_from_gcs
from app.models import db
from app.models.follow import Follow


def get_profile(current_user):
    if not current_user:
        return api_response(message='User not found', status=404)

    return api_response(data=current_user.to_dict(include_email=True), message='Profile retrieved successfully', status=200)


def update_profile(current_user, data):
    allowed_fields = ['full_name', 'email', 'username', 'bio']
    fields_to_update = {k: v for k, v in data.items() if k in allowed_fields and v}

    if not current_user:
        return api_response(message='User not found', status=404)

    # If no fields to update, return error
    if not fields_to_update:
        return api_response(message="No fields to update", status=400)

    # Update profile
    # Check if username or email already exists
    if 'username' in fields_to_update and fields_to_update['username'] != current_user.username:
        if User.query.filter_by(username=fields_to_update['username']).first():
            return api_response(message="Username already exists", status=400)

    if 'email' in fields_to_update and fields_to_update['email'] != current_user.email:
        if User.query.filter_by(email=fields_to_update['email']).first():
            return api_response(message="Email already exists", status=400)

    if 'email' in data:
        if '@' not in data['email']:
            return api_response(message="Invalid email format", status=400)

    #update info
    for key, value in fields_to_update.items():
        setattr(current_user, key, value)

    # Handle profile image upload
    if 'profile_image' in request.files:
        profile_image = request.files['profile_image']
        if profile_image.filename:
            # Delete old image if exists
            if current_user.profile_image:
                delete_file_from_gcs(current_user.profile_image)

            # Upload new image
            image_url = upload_file_to_gcs(profile_image, folder='profile_images')
            if image_url:
                current_user.profile_image = image_url

    try:
        db.session.commit()
        return api_response(message='Profile updated successfully', data=current_user.to_dict(include_email=True))
    except Exception as e:
        db.session.rollback()
        return api_response(message=f"Error updating profile: {str(e)}", status=500)


def get_user_profile(current_user, user_id):
    user = User.query.get(user_id)

    if not user:
        return api_response(message="User not found", status=404)

    # Nếu user đang tự xem profile của chính mình, cho phép hiện cả email
    include_email = current_user.id == user.id

    user_data = user.to_dict(include_email=include_email)

    user_data['is_following'] = current_user.is_following(user)
    user_data['is_followed_by'] = current_user.is_followed_by(user)

    return api_response(data=user_data, message="User profile fetched successfully")


def follow_single_user(current_user, user_id):
    if current_user.id == user_id:
        return api_response(message="You cannot follow yourself", status=400)

    user_to_follow = User.query.get(user_id)
    if not user_to_follow:
        return api_response(message="User not found", status=404)

    if current_user.follow(user_to_follow):
        db.session.commit()
        return api_response(message=f"You are now following {user_to_follow.username}")
    else:
        return api_response(message=f"You are already following {user_to_follow.username}")


def unfollow_single_user(current_user, user_id):
    if current_user.id == user_id:
        return api_response(message="You cannot unfollow yourself", status=400)

    user_to_unfollow = User.query.get(user_id)
    if not user_to_unfollow:
        return api_response(message="User not found", status=404)

    if current_user.unfollow(user_to_unfollow):
        db.session.commit()
        return api_response(message=f"You have unfollowed {user_to_unfollow.username}")
    else:
        return api_response(message=f"You are not following {user_to_unfollow.username}")


def get_followers(user_id):
    user = User.query.get(user_id)
    if not user:
        return api_response(message="User not found", status=404)

    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)

    followers_query = user.followers.join(User, User.id == Follow.follower_id).with_entities(User).paginate(page=page, per_page=per_page)

    followers = [u.to_dict() for u in followers_query.items]

    data_response = {
        'followers': followers,
        'total': followers_query.total,
        'pages': followers_query.pages,
        'page': page
    }

    return api_response(data=data_response)


def get_following(user_id):
    user = User.query.get(user_id)
    if not user:
        return api_response(message="User not found", status=404)

    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)

    following_query = user.following.join(User, User.id == Follow.followed_id).with_entities(User).paginate(page=page, per_page=per_page)

    following = [u.to_dict() for u in following_query.items]

    data_response = {
        'following': following,
        'total': following_query.total,
        'pages': following_query.pages,
        'page': page
    }

    return api_response(data=data_response)


def search_any_users():
    query = request.args.get('q', '')
    if not query or len(query) < 2:
        return api_response(message='Search query must be at least 2 characters', status=400)

    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)

    # Search by username or fullname
    users_query = User.query.filter(
        (User.username.like(f'%{query}%')) | (User.full_name.like(f'%{query}%'))
    ).paginate(page=page, per_page=per_page)

    users = [u.to_dict() for u in users_query.items]

    data_response = {
        'users': users,
        'total': users_query.total,
        'pages': users_query.pages,
        'page': page
    }

    return api_response(data=data_response, message="Search successfully")

