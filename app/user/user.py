from sqlalchemy import func
from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required, logout_user, current_user
from app.models import db, User, Article, Comment, ArticleLike
from app.webforms import UserForm

blueprint = Blueprint("user", __name__, template_folder="templates")

"""
USER Routes:
=> dashboard : INCOMPLETE
    - required (login_required, current_user)
    - context (user, articles, comments(count))
    - pages (dashboard)
=> update_user : INCOMPLETE
    - required (login_required, current_user)
    - pages (dashboard) 
=> deactivate_user 
    - required (login_required, current_user)
    - templates (dashboard)
    - return template (index, login, sign-up)
"""


# Dashboard Page Routing
@blueprint.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    user = User.query.get_or_404(current_user.id)

    # To get all published and not deleted (from users) articles.
    articles = db.session.query(Article).\
        filter(Article.author_id == current_user.id, Article.is_deleted == False).\
        order_by(Article.date_posted.desc()).all()

    # To get the counts of comments and likes for all articles.
    comment_likes_cnts = db.session.query(Article.id.label("article_id"), func.count(Comment.comment).label("comments_count"), func.count(ArticleLike.user_id).label("likes_count")). \
        outerjoin(Comment, Comment.article_id == Article.id). \
        outerjoin(ArticleLike, ArticleLike.article_id == Article.id). \
        group_by(Article.id).all()

    context = {
        "user": user,
        "articles": articles,
        "comment_likes_cnts": comment_likes_cnts,
    }

    return render_template("dashboard.html", **context)


# Edit User Profile Page Routing (done)
@blueprint.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update_user(id):
    form = UserForm()
    user = User.query.get_or_404(id)

    if request.method == "POST" and current_user.id == user.id:
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.about_author = form.about_author.data

        try:
            db.session.commit()
            flash(f"User Profile updated successfully")
            return redirect(url_for("user.dashboard", id=user.id))
        except:
            flash("Something went wrong. Please try again...")
            return redirect(url_for("user.update_user", id=user.id))

    # only the author can edit his article
    if current_user.id == user.id:
        form.firstname.data = user.firstname
        form.lastname.data = user.lastname
        form.about_author.data = user.about_author
    else:
        flash(f"You are not authorized to update this user profile!")
        return redirect(url_for("user.dashboard", id=user.id))

    context = {
        "form": form,
        "user": user,
    }

    return render_template("update-user.html", **context)


# DEACTIVATE USER PROFILE Route (done)
@blueprint.route("/deactivate/<int:id>", methods=["GET", "POST"])
@login_required
def deactivate_user(id):
    user = User.query.get_or_404(id)

    if current_user.id == user.id:
        user.is_active = False
        try:
            db.session.commit()

            logout_user()
            flash(f"User: '{user.username}' deactivated successfully and will be deleted after 30 days, if not reactivated!")
            return redirect(url_for("auth.sign_up"))
        except:
            logout_user()
            flash("Whoops! Something went wrong! Please try again...!")
            return redirect(url_for("auth.login"))
    else:
        flash(f"You are not authorized to deactivate this User: '{user.username}'")
        articles = Article.query.order_by(Article.date_posted.desc()).all
        return redirect(url_for("general.index", articles=articles))
