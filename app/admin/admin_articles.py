from flask import redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from app.models import db, Article

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
@blueprint.route("/publish/<int:id>", methods=["GET", "POST"])
@login_required
def publish(id):
    article = Article.query.get_or_404(id)

    if current_user.is_authenticated and current_user.is_admin:
        article.is_draft = False
        article.slug = article.slugify_title

        try:
            db.session.commit()
            flash(f"Article: '{article.title}' is now published.")
            return redirect(url_for("admin.admin"))
        except:
            flash(f"Whoops! Something went wrong. Please try again!")
            return redirect(url_for("admin.admin"))


# UNPUBLISH ARTICLE
@blueprint.route("/unpublish/<int:id>", methods=["GET", "POST"])
@login_required
def unpublish(id):
    article = Article.query.get_or_404(id)

    if current_user.is_authenticated and current_user.is_admin:
        article.is_draft = True
        article.slug = None

        try:
            db.session.commit()
            flash(f"Article: '{article.title}' is now unpublished.")
            return redirect(url_for("admin.admin"))
        except:
            flash(f"Whoops! Something went wrong. Please try again!")
            return redirect(url_for("admin.admin"))


# DELETE ARTICLE FROM DATABASE
@blueprint.route("/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete(id):
    article = Article.query.get_or_404(id)

    if current_user.is_authenticated and current_user.is_admin:
        try:
            db.session.delete(article)
            db.session.commit()
            flash(f"Article: '{article.title}' is deleted successfully.")
            return redirect(url_for("admin.admin"))
        except:
            flash(f"Whoops! Something went wrong. Please try again!")
            return redirect(url_for("admin.admin"))


# REMOVE ARTICLE FROM USER
@blueprint.route("/remove/<int:id>", methods=["GET", "POST"])
@login_required
def remove(id):
    article = Article.query.get_or_404(id)

    if current_user.is_authenticated and current_user.is_admin:
        article.is_deleted = True
        article.slug = None

        try:
            db.session.commit()
            flash(f"Article: '{article.title}' is removed from user's articles successfully.")
            return redirect(url_for("admin.admin"))
        except:
            flash(f"Whoops! Something went wrong. Please try again!")
            return redirect(url_for("admin.admin"))


# ADD ARTICLE TO USER
@blueprint.route("/add/<int:id>", methods=["GET", "POST"])
@login_required
def add(id):
    article = Article.query.get_or_404(id)

    if current_user.is_authenticated and current_user.is_admin:
        article.is_deleted = False
        article.slug = article.slugify_title

        try:
            db.session.commit()
            flash(f"Article: '{article.title}' is added to user's articles successfully.")
            return redirect(url_for("admin.admin"))
        except:
            flash(f"Whoops! Something went wrong. Please try again!")
            return redirect(url_for("admin.admin"))
