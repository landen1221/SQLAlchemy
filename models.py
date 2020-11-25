"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    image_url = db.Column(db.Text, default="https://www.publicdomainpictures.net/pictures/280000/velka/not-found-image-15383864787lu.jpg")

    def __repr__(self):
        return f"<{self.first_name} / {self.last_name} / {self.image_url[0:10]}>"


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    title = db.Column(db.Text, default="No title provided")
    content= db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    userID = db.relationship('Users', backref='posts')

    post_tag = db.relationship('Tag', secondary="post_tags", backref='posts')

    def __repr__(self):
        return f"<{self.title} / {self.content[:15]} / {self.created_at} / {self.user_id}>"

class PostTag(db.Model):
    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), nullable=False, primary_key=True)

    def __repr__(self):
        return f"<{self.post_id} / {self.tag_id}>"

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_name = db.Column(db.Text, nullable=False, unique=True)

    def __repr__(self):
        return f"<{self.id} / {self.tag_name}>"

