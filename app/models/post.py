from app.models import db
from app.utils.helpers import utc_now


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.Text)
    image_url = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    #Relationships
    likes = db.relationship('Like', backref='post', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, caption, image_url, user_id):
        self.caption = caption
        self.image_url = image_url
        self.user_id = user_id

    def __repr__(self):
        return f''

    def to_dict(self, include_user=False):
        data = {
            'id': self.id,
            'caption': self.caption,
            'image_url': self.image_url,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'like_count': self.likes.count(),
            'liked_by_current_user': False      # Default value, will be updated in controller
        }

        if include_user and self.author:
            data['user'] = self.author.to_dict()

        return data




