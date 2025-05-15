from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.models import init_app as init_db
from app.routes import init_app as init_routes
import config
from app.utils.helpers import api_response



def created_app(test_config=None):
    app = Flask(__name__)

    # Load config
    app.config.from_object(config.Config)

    # Initialize extensions
    jwt = JWTManager(app)

    # Enable CORS
    CORS(app)

    # Initialize database
    init_db(app)

    # Initialize routes
    init_routes(app)

    @jwt.unauthorized_loader
    def missing_token_callback(callback):
        return api_response(message="Authentication required", status=401)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return api_response(message="Token has expired", status=401)

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        return api_response(message=f"Invalid token: {reason}", status=401)


    # Route chính
    @app.route('/')
    def index():
        return api_response(message="Welcome to Instagram Clone API")

    @app.errorhandler(404)
    def not_found(e):
        return api_response(message=f"Endpoint not found: {e}", status=404)

    @app.errorhandler(500)
    def server_error(e):
        return api_response(message=f"Internal server error {e}", status=500)

    return app







