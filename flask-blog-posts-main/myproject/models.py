from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from myproject.extentions import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(64), default='default_profile.jpg')
    email = db.Column(db.String(80), nullable=False, unique=True, index=True)
    username = db.Column(db.String(80), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.Text, nullable=False)

    posts = db.relationship('BlogPost', backref='author', lazy=True)


    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"Username {self.username}"

class BlogPost(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    #users = db.relationship(User)

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return f"Post ID: {self.id}, Date: ({self.date}), {self.text} "

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_post(self):
        db.session.add(self)
        db.session.commit()