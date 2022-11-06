from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import EqualTo, Length, InputRequired
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditor, CKEditorField
from models import app


# Configuring CKEditor
app.config["CKEDITOR_HEIGHT"] = 400
app.config["CKEDITOR_WIDTH"] = 2000

ckeditor = CKEditor(app)


# Create UserForm Class
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
            Length(
                min=5, max=25, message="Password must be between 5 and 15 characters"
            ),
        ],
    )
    email = StringField(
        label="Email",
        validators=[
            InputRequired(message="*Required"),
            Length(
                5, 120, message="Password must be between 5 and 120 characters"
            ),
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
    about_author = TextAreaField(label="About Author", widget=TextArea())
    is_admin = BooleanField(label="Set as Admin")
    submit = SubmitField(label="Submit")


# Create Login Form Class
class LoginForm(FlaskForm):
    username_email = StringField(
        label="Username/Email",
        validators=[
            InputRequired(message="*Required"),
            Length(
                min=5, max=120, message="Password must be between 5 and 15 characters"
            ),
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


# Create Article Form
class ArticleForm(FlaskForm):
    title = StringField(label="Title", validators=[InputRequired()])
    content = CKEditorField(label="Content", validators=[InputRequired()])
    slug = StringField(label="Slug")
    is_draft = BooleanField(label="Save as Draft", default=False)
    submit = SubmitField(label="Submit")


# Create Edit Article Form
class CommentForm(FlaskForm):
    comment = TextAreaField(
        label="Add Comment Here", validators=[InputRequired()], widget=TextArea()
    )
    submit = SubmitField(label="Submit")


# Create Message Form
class MessageForm(FlaskForm):
    name = StringField(label="Name", validators=[InputRequired()])
    email = StringField(label="Email", validators=[InputRequired(message="*Required")])
    message = TextAreaField(
        label="Message", validators=[InputRequired()], widget=TextArea()
    )
    submit = SubmitField(label="Send")
