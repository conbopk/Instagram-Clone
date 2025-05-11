import os
from flask import Flask
from flask_jwt_extended import JWTManager
from app.utils.helpers import api_response
from datetime import timedelta


def created_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev_secret_key"),
        JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY", "jwt_secret_key"),
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=24),
    )

    # Khởi tạo JWT Manager
    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    def missing_token_callback(callback):
        return api_response(message="Authentication required", status=401)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return api_response(message="Token has expired", status=401)

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        return api_response(message=f"Invalid token: {reason}", status=401)

    # Đăng ký các route
    from app.routes.auth_routes import auth_bp
    from app.routes.user_routes import user_bp
    from app.routes.post_routes import post_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(post_bp)

    # Route chính
    @app.route('/')
    def index():
        return api_response(message="Welcome to Instagram Clone API")

    @app.errorhandler(404)
    def not_found(e):
        return api_response(message="Endpoint not found", status=404)

    return app







