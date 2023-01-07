from flask import Flask
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from app.models import db, User
from app import settings, auth, user, article, general, like, admin, admin_users, admin_articles, comment
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from datetime import timedelta

app = Flask(__name__)

# SQLALCHEMY CONFIG
app.config["SQLALCHEMY_DATABASE_URI"] = settings.database_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = settings.secret_key
# Init DB
db.init_app(app)

# # JWT CONFIG FOR AUTH SESSIONS
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=int(settings.access_token_expires))
# app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=int(settings.refresh_token_expires))
# # Init JWT
# jwt = JWTManager(app)

# CKEDITOR CONFIG FOR WEB FORMS
app.config["CKEDITOR_PKG_TYPE"] = settings.package_type
app.config["CKEDITOR_SERVE_LOCAL"] = settings.serve_local
app.config["CKEDITOR_HEIGHT"] = settings.height
app.config["CKEDITOR_WIDTH"] = settings.width
# Init CKEditor
ckeditor = CKEditor(app)

# Init Migrate
migrate = Migrate(app, db, render_as_batch=True)

# LOGIN MANAGER SET UP
login_man = LoginManager(app)
login_man.login_view = "login"


@login_man.user_loader
def user_loader(id):
    return User.query.get(int(id))


# IMAGE UPLOAD CONFIG
app.config['UPLOAD_FOLDER'] = settings.upload_folder
app.config["ALLOWED_EXTENSIONS"] = settings.allowed_extensions

# # CREATE ALL DB TABLES
# with app.app_context():
#     db.create_all()

# REGISTER BLUEPRINTS
app.register_blueprint(user.blueprint, url_prefix="/user")
app.register_blueprint(auth.blueprint, url_prefix="")
app.register_blueprint(article.blueprint, url_prefix="/article")
app.register_blueprint(general.blueprint, url_prefix="")
app.register_blueprint(comment.blueprint, url_prefix="/comment")
app.register_blueprint(like.blueprint, url_prefix="/like")
app.register_blueprint(admin.blueprint, url_prefix="/admin")
app.register_blueprint(admin_users.blueprint, url_prefix="/admin-user")
app.register_blueprint(admin_articles.blueprint, url_prefix="/admin-article")
