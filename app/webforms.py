from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField#, FileField
from flask_wtf.file import FileField
from wtforms.validators import EqualTo, Length, InputRequired
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField


# User Form Class
class UserForm(FlaskForm):
    firstname = StringField(
        label="First Name", validators=[InputRequired(message="*Required")]
    )
    lastname = StringField(
        label="Last Name", validators=[InputRequired(message="*Required")]
    )
    username = StringField(
        label="Username",
        validators=[
            InputRequired(message="*Required"),
            Length(5, 25, message="Password must be between 5 and 15 characters"),
        ],
    )
    email = StringField(
        label="Email",
        validators=[
            InputRequired(message="*Required"),
            Length(5, 120, message="Password must be between 5 and 120 characters"),
        ],
    )
    password = PasswordField(
        label="Password",
        validators=[
            InputRequired(message="*Required"),
            Length(min=8, message="Password must be more than 8 characters"),
        ],
    )
    confirm_password = PasswordField(
        label="Confirm Password",
        validators=[
            InputRequired(message="*Required"),
            EqualTo("password", message="Passwords do not match!"),
        ],
    )
    bio = TextAreaField(label="Bio", widget=TextArea())
    profile_pic = FileField(label="Profile Picture")
    is_admin = BooleanField(label="Set as Admin")
    submit = SubmitField(label="Submit")


# Login Form Class
class LoginForm(FlaskForm):
    username_email = StringField(
        label="Username/Email",
        validators=[
            InputRequired(message="*Required"),
            Length(5, 120, message="Password must be between 5 and 15 characters"),
        ],
    )
    password = PasswordField(
        label="Password",
        validators=[
            InputRequired(message="*Required"),
            Length(min=8, message="Password must be more than 8 characters"),
        ],
    )
    submit = SubmitField(label="Login")


# ARTICLE FORM
class ArticleForm(FlaskForm):
    title = StringField(label="Title", validators=[InputRequired()])
    content = CKEditorField(label="Content", validators=[InputRequired()])
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
    name = StringField(label="Name", validators=[InputRequired()])
    email = StringField(label="Email", validators=[InputRequired(message="*Required")])
    message = TextAreaField(
        label="Message", validators=[InputRequired()], widget=TextArea()
    )
    submit = SubmitField(label="Send")
