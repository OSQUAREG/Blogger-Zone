from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField, EmailField
from flask_wtf.file import FileField
from wtforms.validators import EqualTo, Length, InputRequired
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField


# USER FORM
class UserForm(FlaskForm):
    firstname = StringField(
        label="First Name", validators=[InputRequired(message="* Required")]
    )
    lastname = StringField(
        label="Last Name", validators=[InputRequired(message="* Required")]
    )
    username = StringField(
        label="Username",
        validators=[
            InputRequired(message="* Required"),
            Length(5, 25, message="Password must be between 5 and 15 characters"),
        ],
    )
    email = EmailField(
        label="Email",
        validators=[
            InputRequired(message="* Required"),
            Length(5, 120, message="Password must be between 5 and 120 characters"),
        ],
    )
    password = PasswordField(
        label="Password",
        validators=[
            InputRequired(message="* Required"),
            Length(min=8, message="Password must be more than 8 characters"),
        ],
    )
    confirm_password = PasswordField(
        label="Confirm Password",
        validators=[
            InputRequired(message="* Required"),
            EqualTo("password", message="Passwords do not match!"),
        ],
    )
    bio = TextAreaField(label="Bio", widget=TextArea())
    profile_pic = FileField(label="Profile Picture")
    is_admin = BooleanField(label="Set as Admin")
    submit = SubmitField(label="Submit")


# LOGIN FORM
class LoginForm(FlaskForm):
    username_email = StringField(
        label="Username/Email",
        validators=[InputRequired(message="* Required")],
    )
    password = PasswordField(
        label="Password",
        validators=[InputRequired(message="* Required")],
    )
    submit = SubmitField(label="Login")


# ARTICLE FORM
class ArticleForm(FlaskForm):
    title = StringField(label="Title", validators=[InputRequired(message="* Required")])
    content = CKEditorField(label="Content", validators=[InputRequired(message="* Required")])
    is_draft = BooleanField(label="Save as Draft", default=False)
    submit = SubmitField(label="Submit")


# COMMENT FORM
class CommentForm(FlaskForm):
    comment = TextAreaField(
        label="Add Comment Here", validators=[InputRequired()], widget=TextArea()
    )
    submit = SubmitField(label="Submit")


# MESSAGE FORM
class MessageForm(FlaskForm):
    name = StringField(label="Name", validators=[InputRequired(message="* Required")])
    email = EmailField(label="Email", validators=[InputRequired(message="*Required")])
    message = TextAreaField(
        label="Message", validators=[InputRequired()], widget=TextArea()
    )
    submit = SubmitField(label="Send")


# SEARCH FORM
class SearchForm(FlaskForm):
    search_word = StringField(label="Search Here", validators=[InputRequired()])
    submit = SubmitField(label="Search")


# CHANGE PASSWORD FORM
class PasswordForm(FlaskForm):
    old_password = PasswordField(
        label="Old Password",
        validators=[InputRequired(message="* Required")],
    )
    new_password = PasswordField(
        label="New Password",
        validators=[
            InputRequired(message="* Required"),
            Length(min=8, message="Password must be more than 8 characters"),
        ],
    )
    confirm_new_password = PasswordField(
        label="Confirm New Password",
        validators=[
            InputRequired(message="* Required"),
            EqualTo("new_password", message="Passwords do not match!"),
        ],
    )
    submit = SubmitField(label="Submit")
