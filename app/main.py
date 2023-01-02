from flask import Flask
from flask_login import LoginManager
from flask_ckeditor import CKEditor

from app.models import db, User
from app import settings, auth, user, article, general, admin_users
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from datetime import timedelta

app = Flask(__name__)

# SQLALCHEMY CONFIG
app.config["SQLALCHEMY_DATABASE_URI"] = settings.database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = settings.secret_key

# JWT CONFIG FOR AUTH SESSIONS
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=int(settings.access_token_expires))
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=int(settings.refresh_token_expires))

# CKEDITOR CONFIG FOR WEB FORMS
app.config["CKEDITOR_HEIGHT"] = 400
app.config["CKEDITOR_WIDTH"] = 2000

db.init_app(app)

# INIT MIGRATE
migrate = Migrate(app, db, render_as_batch=True)

# INIT JWT MANAGER
jwt = JWTManager(app)

# INIT CKEDITOR
ckeditor = CKEditor(app)


# LOGIN MANAGER SET UP
login_man = LoginManager(app)
login_man.login_view = "login"


@login_man.user_loader
def user_loader(id):
    return User.query.get(int(id))


# # CREATE ALL DB TABLES
# with app.app_context():
#     db.create_all()

app.register_blueprint(user.blueprint, url_prefix="/user")
app.register_blueprint(auth.blueprint, url_prefix="")
app.register_blueprint(article.blueprint, url_prefix="")
app.register_blueprint(general.blueprint, url_prefix="")
app.register_blueprint(admin_users.blueprint, url_prefix="/admin")
