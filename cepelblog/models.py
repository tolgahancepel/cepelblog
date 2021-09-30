"""
cepelblog/models.py
"""

from datetime import datetime
from cepelblog import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin # is  authenticated

# Login Manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Tags and Posts Relationship
tag_post_table = db.Table('tag_post', db.Model.metadata,
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('blogposts.id'))
)

# -----------------------------------------------------------------------------
# USER TABLE
# -----------------------------------------------------------------------------

class User(db.Model, UserMixin):
    
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return self.username

# -----------------------------------------------------------------------------
# BLOGPOST TABLE
# -----------------------------------------------------------------------------

class BlogPost(db.Model):
    
    __tablename__ = "blogposts"
    
    users = db.relationship('User')
    tags = db.relationship('Tag', secondary=tag_post_table)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    banner_image = db.Column(db.String(64), nullable=False, default='default_banner.png')
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, title, text, user_id, tags):
        self.title = title
        self.text = text
        self.user_id = user_id
        self.tags = tags
    
    def __repr__(self):
        return f"Post ID: {self.id} -- Date : {self.date} -- Title: {self.title}"

# -----------------------------------------------------------------------------
# TAG TABLE
# -----------------------------------------------------------------------------

class Tag(db.Model):

    __tablename__ = "tags"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return self.name