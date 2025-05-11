from datetime import datetime
from app.utils.helpers import api_response


# Giả lập database cho posts
posts_db = {}
post_id_counter = 1

def create_post(username, data):
    global post_id_counter

    caption = data.get('caption', '')
    image_url = data.get('image_url')

    if not image_url:
        return api_response(message='Image URL is required', status=400)

    post_id = post_id_counter
    post_id_counter += 1

    post = {
        'id': post_id,
        'user': username,
        'caption': caption,
        'image_url': image_url,
        'likes': 0,
        'comments': [],
        'created_at': int(datetime.now().timestamp())
    }

    posts_db[post_id] = post

    return api_response(data=post, message='Post created successfully')


def get_post(post_id):
    post = posts_db.get(int(post_id))
    if not post:
        return api_response(message='Post not found', status=404)

    return api_response(data=post, message='Post retrieved successfully')

def delete_post(username, post_id):
    post_id = int(post_id)
    post = posts_db.get(post_id)

    if not post:
        return api_response(message='Post not found', status=404)

    if post['user'] != username:
        return api_response(message='Not authorized to delete this post', status=403)

    del posts_db[post_id]

    return api_response(message="Post deleted successfully")


def like_post(username, post_id):
    post_id = int(post_id)
    post = posts_db.get(post_id)

    if not post:
        return api_response(message='Post not found', status=404)

    post['like'] += 1

    return api_response(data=post, message='Post liked successfully')

def get_user_posts(username):
    user_posts = []
    for post_id, post in posts_db.items():
        if post['user'] == username:
            user_posts.append(post)

    user_posts.sort(key=lambda x: x['created_at'], reverse=True)

    return api_response(data=user_posts, message='Posts retrieved successfully')






