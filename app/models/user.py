from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash



# Giả lập database với dict
users_db = {}


class User:
    def __init__(self, username, email, full_name, password=None):
        self.username = username
        self.email = email
        self.full_name = full_name
        self.profile_picture = 'static/images/default.png'
        self.bio = ''
        self.created_at = int(datetime.now().timestamp())
        self._password_hash = generate_password_hash(password) if password else None

    def check_password(self, password):
        return check_password_hash(self._password_hash, password)

    def save(self):
        # Lưu user vào database
        users_db[self.username] = {
            'password': self._password_hash,
            'profile': self.to_dict()
        }
        return self

    @staticmethod
    def get_by_username(username):
        user_data = users_db.get(username)
        if not user_data:
            return None

        user = User(
            username=username,
            email=user_data['profile']['email'],
            full_name=user_data['profile']['full_name']
        )
        user._password_hash = user_data['password']
        user.profile_picture = user_data['profile'].get('profile_picture', '/static/images/default.png')
        user.bio = user_data['profile']['bio']
        user.created_at = user_data['profile']['created_at']

        return user


    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'bio': self.bio,
            'created_at': self.created_at,
            'profile_picture': self.profile_picture
        }

