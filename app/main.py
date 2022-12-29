from flask import Flask
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from app.models import db, User
from app import settings, auth, user, article, general

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = settings.database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = settings.secret_key

db.init_app(app)

# CKEDITOR CONFIG FOR WEB FORMS
app.config["CKEDITOR_HEIGHT"] = 400
app.config["CKEDITOR_WIDTH"] = 2000
ckeditor = CKEditor(app)

# LOGIN MANAGER SET UP
login_man = LoginManager(app)
login_man.login_view = "login"


@login_man.user_loader
def user_loader(id):
    return User.query.get(int(id))


# Create all DB tables
with app.app_context():
    db.create_all()

app.register_blueprint(general.blueprint, url_prefix="")
app.register_blueprint(user.blueprint, url_prefix="")
app.register_blueprint(article.blueprint, url_prefix="")
app.register_blueprint(auth.blueprint, url_prefix="")
