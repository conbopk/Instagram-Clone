from app.routes.auth_routes import auth_bp
from app.routes.user_routes import user_bp
from app.routes.post_routes import post_bp


def init_app(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(post_bp)
