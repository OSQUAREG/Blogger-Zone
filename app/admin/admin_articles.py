from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User, Article
from app.webforms import UserForm
# from datetime import timedelta

blueprint = Blueprint("admin-articles", __name__, template_folder="templates")

"""
AUTH Routes:
=> publish_article : COMPLETE
    - required (current_user.is_admin)
    - templates (admin)
=> unpublish_article : COMPLETE
    - required (current_user.is_admin)
    - templates (admin)
=> delete_article : COMPLETE
    - required (current_user.is_admin)
    - templates (admin)
=> remove_article : COMPLETE
    - required (current_user.is_admin)
    - templates (admin)
=> add_article : COMPLETE
    - required (current_user.is_admin)
    - templates (admin)

"""


# PUBLISH ARTICLE
@blueprint.route("/publish-article/<int:id>", methods=["GET", "POST"])
@login_required
def publish_article(id):
    article = Article.query.get_or_404(id)

    if current_user.is_authenticated and current_user.is_admin:
        article.is_draft = False

        try:
            db.session.commit()
            flash(f"Article: '{article.title}' is now published.")
            return redirect(url_for("admin-users.admin"))
        except:
            flash(f"Whoops! Something went wrong. Please try again!")
            return redirect(url_for("admin-users.admin"))


# UNPUBLISH ARTICLE
@blueprint.route("/unpublish-article/<int:id>", methods=["GET", "POST"])
@login_required
def unpublish_article(id):
    article = Article.query.get_or_404(id)

    if current_user.is_authenticated and current_user.is_admin:
        article.is_draft = True

        try:
            db.session.commit()
            flash(f"Article: '{article.title}' is now unpublished.")
            return redirect(url_for("admin-users.admin"))
        except:
            flash(f"Whoops! Something went wrong. Please try again!")
            return redirect(url_for("admin-users.admin"))


# DELETE ARTICLE FROM DATABASE
@blueprint.route("/delete-from-db/<int:id>", methods=["GET", "POST"])
@login_required
def delete_article(id):
    article = Article.query.get_or_404(id)

    if current_user.is_authenticated and current_user.is_admin:
        try:
            db.sessoin.delete(article)
            db.session.commit()
            flash(f"Article: '{article.title}' is deleted successfully.")
            return redirect(url_for("admin-users.admin"))
        except:
            flash(f"Whoops! Something went wrong. Please try again!")
            return redirect(url_for("admin-users.admin"))


# REMOVE ARTICLE FROM USER
@blueprint.route("/remove-article/<int:id>", methods=["GET", "POST"])
@login_required
def remove_article(id):
    article = Article.query.get_or_404(id)

    if current_user.is_authenticated and current_user.is_admin:
        article.is_deleted = True
        try:
            db.session.commit()
            flash(f"Article: '{article.title}' is removed from user's articles successfully.")
            return redirect(url_for("admin-users.admin"))
        except:
            flash(f"Whoops! Something went wrong. Please try again!")
            return redirect(url_for("admin-users.admin"))


# ADD ARTICLE TO USER
@blueprint.route("/add-article/<int:id>", methods=["GET", "POST"])
@login_required
def add_article(id):
    article = Article.query.get_or_404(id)

    if current_user.is_authenticated and current_user.is_admin:
        article.is_deleted = False
        try:
            db.session.commit()
            flash(f"Article: '{article.title}' is added to user's articles successfully.")
            return redirect(url_for("admin-users.admin"))
        except:
            flash(f"Whoops! Something went wrong. Please try again!")
            return redirect(url_for("admin-users.admin"))
