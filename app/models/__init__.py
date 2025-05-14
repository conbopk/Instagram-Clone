from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)

    # Import all models
    from app.models.user import User
    from app.models.post import Post
    from app.models.follow import Follow
    from app.models.like import Like

    # Create tables
    with app.app_context():
        db.create_all()



