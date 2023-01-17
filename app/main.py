from flask import Flask, render_template
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from app.models import db, User
from app import sett, auth, user, article, general, like, admin, admin_users, admin_articles, comment
from flask_migrate import Migrate

# from flask_jwt_extended import JWTManager
# from datetime import timedelta

app = Flask(__name__)

# SQLALCHEMY CONFIG
app.config["SQLALCHEMY_DATABASE_URI"] = sett.database_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = sett.track_modifications
app.config["SECRET_KEY"] = sett.secret_key

# Init DB
db.init_app(app)

# Init Migrate
migrate = Migrate(app, db, render_as_batch=False)

# # JWT CONFIG FOR AUTH SESSIONS
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=int(settings.access_token_expires))
# app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=int(settings.refresh_token_expires))
# # Init JWT
# jwt = JWTManager(app)

# CKEDITOR CONFIG FOR WEB FORMS
app.config["CKEDITOR_PKG_TYPE"] = sett.package_type
app.config["CKEDITOR_SERVE_LOCAL"] = sett.serve_local
app.config["CKEDITOR_HEIGHT"] = sett.height
app.config["CKEDITOR_WIDTH"] = sett.width

# Init CKEditor
ckeditor = CKEditor(app)

# LOGIN MANAGER SET UP
login_man = LoginManager(app)
login_man.login_view = "login"


@login_man.user_loader
def user_loader(id):
    return User.query.get(int(id))


# IMAGE UPLOAD CONFIG
app.config['UPLOAD_FOLDER'] = sett.upload_folder
app.config["ALLOWED_EXTENSIONS"] = sett.allowed_extensions

# PAGINATION CONFIG
app.config["PER_PAGE"] = sett.per_page

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


# CUSTOM ERROR HANDLERS
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
