from flask import Flask, render_template, session
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from app.models import db, User
from app import sett, auth, user, article, general, like, admin, admin_users, admin_articles, comment
from flask_migrate import Migrate
from datetime import timedelta

app = Flask(__name__)

# SQLALCHEMY CONFIG
app.config["SQLALCHEMY_DATABASE_URI"] = sett.database_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = sett.track_modifications
app.config["SECRET_KEY"] = sett.secret_key

# Init DB
db.init_app(app)

# Instantiate Migrate
migrate = Migrate(app, db, render_as_batch=False)

# CKEDITOR CONFIG FOR WEB FORMS
app.config["CKEDITOR_PKG_TYPE"] = sett.package_type
app.config["CKEDITOR_SERVE_LOCAL"] = sett.serve_local
app.config["CKEDITOR_HEIGHT"] = sett.height
app.config["CKEDITOR_WIDTH"] = sett.width

# Instantiate CKEditor
ckeditor = CKEditor(app)

# FLASK LOGIN CONFIG
login_man = LoginManager(app)
login_man.login_view = "auth.login"
login_man.refresh_view = "accounts.reauthenticate"
login_man.needs_refresh_message = (u"Session timed out, please re-login")
login_man.needs_refresh_message_category = "info"


@login_man.user_loader
def user_loader(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=int(sett.login_session_minutes))


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
