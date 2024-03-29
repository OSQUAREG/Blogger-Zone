from flask_sqlalchemy import SQLAlchemy
from slugify import slugify
from sqlalchemy import MetaData
from flask_login import UserMixin
from datetime import datetime

# CREATE CUSTOM METADATA - NAMING CONVENTION FOR CONSTRAINTS
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=naming_convention)
db = SQLAlchemy(metadata=metadata)


# USER MODEL/TABLE
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.Text(150), nullable=False, unique=True)
    password_hash = db.Column(db.Text(255), nullable=False, unique=True)
    bio = db.Column(db.Text(), nullable=True)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    profile_pic = db.Column(db.String(), nullable=True)
    last_updated_by = db.Column(db.String)
    last_updated_on = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # create relationship to articles, comments & likes
    articles = db.relationship("Article", backref="author")
    comments = db.relationship("Comment", backref="commenter")
    article_likes = db.relationship("ArticleLike", backref="art_liker")
    comment_likes = db.relationship("CommentLike", backref="com_liker")

    def __repr__(self):
        return f"User: <{self.username}>"


# ARTICLE MODEL/TABLE
class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(255), nullable=True)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    is_draft = db.Column(db.Boolean, default=False, nullable=False)
    last_updated_on = db.Column(db.DateTime, onupdate=datetime.utcnow)
    last_updated_by = db.Column(db.String)
    is_deleted = db.Column(db.Boolean, default=False)

    # creates foreign keys with related users (authors).
    author_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))

    # create relationship to comments and likes.
    comments = db.relationship("Comment", backref="articles")
    article_likes = db.relationship("ArticleLike", backref="articles")
    comment_likes = db.relationship("CommentLike", backref="articles")

    def __repr__(self):
        return f"Article: <{self.title}>"

    @property
    def slugify_title(self):
        return slugify(self.title)


# COMMENT MODEL/TABLE
class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text(), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    edited = db.Column(db.Boolean, default=False)

    # create foreign keys with related users and articles.
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id", ondelete="CASCADE"))

    # create relationship to likes.
    likes = db.relationship("CommentLike", backref="comments")

    def __repr__(self):
        return f"Comment by: <{self.user_id}>"


# ARTICLE LIKES MODEL/TABLE
class ArticleLike(db.Model):
    __tablename__ = "article_likes"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id", ondelete="CASCADE"), primary_key=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Article Like by: <{self.user_id}>"


# COMMENT LIKES MODEL/TABLE
class CommentLike(db.Model):
    __tablename__ = "comment_likes"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey("comments.id", ondelete="CASCADE"), primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id", ondelete="CASCADE"))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Comment Like by: <{self.user_id}>"


# MESSAGE MODEL/TABLE
class Message(db.Model):
    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String, nullable=False)
    message = db.Column(db.Text(), nullable=False)
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Send by: <{self.name}>"
