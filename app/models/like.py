from app.models import db
from app.utils.helpers import utc_now


class Like(db.Model):
    __tablename__ = 'likes'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=utc_now)

    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id


