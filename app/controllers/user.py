from app.models.user import User, users_db
from app.utils.helpers import api_response


def get_profile(username):
    user = User.get_by_username(username)
    if not user:
        return api_response(message='User not found', status=404)

    return api_response(data=user.to_dict(), message='Profile retrieved successfully')


def update_profile(username, data):
    user = User.get_by_username(username)
    if not user:
        return api_response(message='User not found', status=404)

    # Cập nhật thông tin
    if 'full_name' in data:
        user.full_name = data['full_name']

    if 'bio' in data:
        user.bio = data['bio']

    if 'email' in data:
        if '@' not in data['email']:
            return api_response(message="Invalid email format", status=400)
        user.email = data['email']

    # Lưu thay đổi
    user.save()

    return api_response(data=user.to_dict(), message='Profile updated successfully')

def update_profile_picture(username, picture_data):
    user = User.get_by_username(username)
    if not user:
        return api_response(message='User not found', status=404)

    # Xử lý upload ảnh (giả lập)
    user.profile_picture = f"{username}.jpg"
    user.save()

    return api_response(data=user.to_dict(), message='Profile picture updated successfully')

def get_all_users():
    # Lấy danh sách tất cả người dùng (chỉ để test)
    user_list = []
    for username, user_data in users_db.items():
        user_list.append(user_data['profile'])

    return api_response(data=user_list, message='Users retrieved successfully')

