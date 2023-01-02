from flask_sqlalchemy import SQLAlchemy
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


# ARTICLE MODEL/TABLE
class Article(db.Model):
    __tablename__ = "articles"
    # __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(20))
    is_draft = db.Column(db.Boolean, default=False, nullable=False)
    last_updated_on = db.Column(db.DateTime, default=datetime.utcnow)

    # creates foreign keys with related users (authors).
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # create relationship to comments and likes.
    comments = db.relationship("Comment", backref="articles")
    likes = db.relationship("ArticleLike", backref="articles")

    def __repr__(self):
        return f"Article: <{self.title}>"


# USER MODEL/TABLE
class User(db.Model, UserMixin):
    __tablename__ = "users"
    # __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.Text(150), nullable=False, unique=True)
    password_hash = db.Column(db.Text(255), nullable=False, unique=True)
    about_author = db.Column(db.Text(), nullable=True)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    # profile_pic = db.Column(db.String(), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    # modified_by = db.Column(db.Integer)
    # modified_on = db.Column(db.DateTime, default=datetime.utcnow)

    # # create foreign key with roles.
    # role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    # create relationship to articles, comments & likes
    articles = db.relationship("Article", backref="author")
    comments = db.relationship("Comment", backref="commenter")
    article_likes = db.relationship("ArticleLike", backref="art_liker")
    comment_likes = db.relationship("CommentLike", backref="com_liker")

    def __repr__(self):
        return f"User: <{self.username}>"


# # USER ROLES MODEL/TABLE
# class UserRole(db.Model):
#     __tablename__ = "roles"
#     # __table_args__ = {'extend_existing': True}
#
#     id = db.Column(db.Integer, primary_key=True)
#     role = db.Column(db.String(20), unique=True, nullable=False)
#     is_super_admin = db.Column(db.Boolean, default=False)
#     is_active = db.Column(db.Boolean, default=True)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)
#
#     # create relationship to users.
#     users = db.relationship("UserRole", backref="roles")


# COMMENT MODEL/TABLE
class Comment(db.Model):
    __tablename__ = "comments"
    # __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text(), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    edited = db.Column(db.Boolean, default=False)

    # create foreign keys with related users and articles.
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id"))

    # create relationship to likes.
    likes = db.relationship("CommentLike", backref="comments")

    def __repr__(self):
        return f"Comment by: <{self.user_id}>"


# ARTICLE LIKES MODEL/TABLE
class ArticleLike(db.Model):
    __tablename__ = "article_likes"
    # __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id", ondelete="CASCADE"), primary_key=True)

    def __repr__(self):
        return f"Article Like by: <{self.user_id}>"


# COMMENT LIKES MODEL/TABLE
class CommentLike(db.Model):
    __tablename__ = "comment_likes"
    # __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey("comments.id", ondelete="CASCADE"), primary_key=True)

    def __repr__(self):
        return f"Comment Like by: <{self.user_id}>"


# MESSAGE MODEL/TABLE
class Message(db.Model):
    __tablename__ = "contact_messages"
    # __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String, nullable=False)
    message = db.Column(db.Text(), nullable=False)
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Send by: <{self.name}>"
