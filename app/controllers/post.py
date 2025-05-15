from flask import request
from sqlalchemy import desc
from app.utils.helpers import api_response
from app.models import db
from app.models.user import User
from app.models.post import Post
from app.models.follow import Follow
from app.models.like import Like
from app.utils.storage import upload_file_to_gcs, delete_file_from_gcs


def create_post(current_user):
    # Check if image is provided
    if 'image' not in request.files:
        return api_response(message="No image provided", status=400)

    image = request.files['image']
    if not image.filename:
        return api_response(message="No image selected", status=400)

    # Upload image to GCS
    image_url = upload_file_to_gcs(image, folder='posts')
    if not image_url:
        return api_response(message='Failed to upload image', status=500)

    # Create post
    caption = request.form.get('caption', '')
    new_post = Post(
        caption=caption,
        image_url=image_url,
        user_id=current_user.id
    )

    db.session.add(new_post)
    db.session.commit()

    post_data = new_post.to_dict(include_user=True)
    return api_response(data=post_data, message='Post created successfully', status=201)


def get_post(current_user, post_id):
    post = Post.query.get(post_id)
    if not post:
        return api_response(message='Post not found', status=404)

    post_data = post.to_dict(include_user=True)
    # Check if current user has liked the post
    post_data['liked_by_current_user'] = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first() is not None

    return api_response(data=post_data, message='Post retrieved successfully')


def delete_post(current_user, post_id):
    post = Post.query.get(post_id)
    if not post:
        return api_response(message='Post not found', status=404)

    if post.user_id != current_user.id:
        return api_response(message='Unauthorized to delete this post', status=403)

    # Delete image from GCS
    if post.image_url:
        delete_file_from_gcs(post.image_url)

    # Delete post from database
    try:
        db.session.delete(post)
        db.session.commit()
        return api_response(message="Post deleted successfully")
    except Exception as e:
        db.session.rollback()
        return api_response(message=f"Error deleting post: {str(e)}", status=500)


def get_user_posts(current_user, user_id):
    user = User.query.get(user_id)
    if not user:
        return api_response(message="User not found", status=404)

    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 50)

    posts_query = Post.query.filter_by(user_id=user_id).order_by(desc(Post.created_at)).paginate(page=page, per_page=per_page)

    # Get likes for current user in one query
    user_likes = set()
    if posts_query.items:
        post_ids = [p.id for p in posts_query.items]
        likes = Like.query.filter(Like.user_id == current_user.id, Like.post_id.in_(post_ids)).all()
        user_likes = {like.post_id for like in likes}

    posts = []
    for post in posts_query.items:
        post_data = post.to_dict(include_user=True)
        post_data['liked_by_current_user'] = post.id in user_likes
        posts.append(post_data)

    data_response = {
        'posts': posts,
        'total': posts_query.total,
        'pages': posts_query.pages,
        'page': page
    }

    return api_response(data=data_response, message='Posts retrieved successfully')


def like_post(current_user, post_id):
    post = Post.query.get(post_id)
    if not post:
        return api_response(message='Post not found', status=404)

    # Check if already liked
    existing_like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()

    if existing_like:
        return api_response(message="Post already liked")

    # Create like
    like = Like(user_id=current_user.id, post_id=post_id)

    try:
        db.session.add(like)
        db.session.commit()
        return api_response(message="Post liked successfully")
    except Exception as e:
        db.session.rollback()
        return api_response(message=f"Error deleting post: {str(e)}", status=500)


def unlike_post(current_user, post_id):
    like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if not like:
        return api_response(message='Post was not liked')

    try:
        db.session.delete(like)
        db.session.commit()
        return api_response(message='Post unliked successfully')
    except Exception as e:
        db.session.rollback()
        return api_response(message=f'Error deleting like: {str(e)}', status=500)


def get_post_likes(post_id):
    post = Post.query.get(post_id)
    if not post:
        return api_response(message="Post not found", status=404)

    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)

    likes_query = Like.query.filter_by(post_id=post_id).join(User).with_entities(User).paginate(page=page, per_page=per_page)
    likes = [u.to_dict() for u in likes_query.items]

    data_response = {
        'users': likes,
        'total': likes_query.total,
        'pages': likes_query.pages,
        'page': page
    }

    return api_response(data=data_response, message='List of users who liked this post retrieved successfully.')


def get_news_feed(current_user):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 50)

    # Get IDs of users that current user follows
    following_subquery = db.session.query(Follow.followed_id).filter(Follow.follower_id == current_user.id)

    # Get posts from followed users and current user
    feed_query = Post.query.filter(
        (Post.user_id.in_(following_subquery)) | (Post.user_id == current_user.id)
    ).order_by(desc(Post.created_at)).paginate(page=page, per_page=per_page)

    # Get likes for current user in one query
    user_likes = set()
    if feed_query.items:
        post_ids = [p.id for p in feed_query.items]
        likes = Like.query.filter(
            Like.user_id == current_user.id,
            Like.post_id.in_(post_ids)
        ).all()
        user_likes = {like.post_id for like in likes}

    posts = []
    for post in feed_query.items:
        post_data = post.to_dict(include_user=True)
        post_data['liked_by_current_user'] = post.id in user_likes
        posts.append(post_data)

    data_response = {
        'posts': posts,
        'total': feed_query.total,
        'pages': feed_query.pages,
        'page': page
    }

    return api_response(data=data_response, message="News feed retrieved successfully")


