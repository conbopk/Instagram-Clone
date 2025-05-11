from app.models.user import User
from app.utils.helpers import api_response
from flask_jwt_extended import create_access_token, create_refresh_token



def register_user(data):
    username = data.get('username')
    password = data.get('password')
    full_name = data.get('full_name')
    email = data.get('email')

    # Kiểm tra dữ liệu đầu vào
    if not username or not password:
        return api_response(message="Missing username or password", status=400)

    # Kiểm tra username đã tồn tại chưa
    if User.get_by_username(username):
        return api_response(message="Username already exists", status=400)

    # Kiểm tra email hợp lệ
    if not email or '@' not in email:
        return api_response(message='Invalid email format', status=400)

    # Kiểm tra độ dài mật khẩu
    if len(password) < 6:
        return api_response(message='Password must be least 6 characters long', status=400)

    # Kiểm tra tên đầy đủ
    if not full_name:
        return api_response(message="Missing full name", status=400)

    # Tạo user mới
    user = User(username=username, email=email, full_name=full_name, password=password)
    user.save()

    return api_response(data=user.to_dict(), message='User registered successfully')

def login_user(data):
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return api_response(message="Missing username or password", status=400)

    user = User.get_by_username(username)
    if not user or not user.check_password(password):
        return api_response(message='Invalid username or password', status=401)

    # Tạo JWT token với flask_jwt_extended
    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    return api_response(
        data={
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        },
        message='Login successful'
    )

def logout_user():
    return api_response(message='Logout successful')


