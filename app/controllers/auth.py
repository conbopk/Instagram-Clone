from app.models.user import User
from app.models import db
from app.utils.helpers import api_response
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta



def register_user(data):
    # Check if fields are present
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return api_response(message=f"Missing required field: {field}", status=400)

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    # Kiểm tra dữ liệu đầu vào
    # Kiểm tra username đã tồn tại chưa
    if User.query.filter_by(username=data['username']).first():
        return api_response(message="Username already exists", status=400)

    # Kiểm tra email hợp lệ
    if User.query.filter_by(email=data['email']).first():
        return api_response(message='Email already exists', status=400)

    if '@' not in email or '.' not in email:
        return api_response(message='Invalid email format', status=400)

    # Kiểm tra độ dài mật khẩu
    if len(password) < 6:
        return api_response(message='Password must be least 6 characters long', status=400)

    # Create new user
    new_user = User(
        username=username,
        email=email,
        password=password,
        full_name=data.get('full_name', ''),
        bio=data.get('bio', '')
    )

    # Add user to database
    db.session.add(new_user)
    db.session.commit()

    return api_response(data=new_user.to_dict(include_email=True), message='User registered successfully', status=201)

def login_user(data):
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return api_response(message="Missing username or password", status=400)

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return api_response(message='Invalid username or password', status=401)

    # Tạo JWT token với flask_jwt_extended
    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
    refresh_token = create_refresh_token(identity=str(user.id), expires_delta=timedelta(days=30))

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


def get_current_user(current_user):
    if not current_user:
        return api_response(message="User not found", status=404)

    return api_response(data=current_user.to_dict(include_email=True), message="User info retrieved successfully", status=200)