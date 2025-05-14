from app.models import db
from app.models.follow import Follow
from app.utils.helpers import utc_now
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    bio = db.Column(db.Text)
    profile_image = db.Column(db.String(255), default='images/default.jpg')
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    # Relationships
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    # Followers relationship (self-referential)
    followers = db.relationship(
        'Follow',
        foreign_keys='Follow.followed_id',
        backref=db.backref('followed', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    following = db.relationship(
        'Follow',
        foreign_keys='Follow.follower_id',
        backref=db.backref('follower', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def __init__(self, username, email, password, full_name=None, bio=None):
        self.username = username
        self.email = email
        self.set_password(password)
        self.full_name = full_name
        self.bio = bio

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_email=False):
        data = {
            'user_id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'bio': self.bio,
            'profile_image': self.profile_image,
            'created_at': self.created_at.isoformat(),
            'follower_count': self.followers.count(),
            'following_count': self.following.count(),
            'post_count': self.posts.count()
        }
        if include_email:
            data['email'] = self.email
        return data

    def follow(self, user):
        if not self.is_following(user):
            follow = Follow(follower_id=self.id, followed_id=user.id)
            db.session.add(follow)
            return True
        return False

    def unfollow(self, user):
        follow = self.following.filter_by(followed_id=user.id).first()
        if follow:
            db.session.delete(follow)
            return True
        return False

    def is_following(self, user):
        return self.following.filter_by(followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id=user.id).first() is not None
