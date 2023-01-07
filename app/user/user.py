from sqlalchemy import func
from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required, logout_user, current_user
from app.models import db, User, Article, Comment, ArticleLike
from app.webforms import UserForm, SearchForm
from app.utils import upload_image

blueprint = Blueprint("user", __name__, template_folder="templates")

"""
USER Routes:
=> dashboard : INCOMPLETE
    - requirement (login_required, current_user)
    - context (user, articles, comments(count))
    - pages (dashboard)
=> update_user : INCOMPLETE
    - requirement (login_required, current_user)
    - pages (dashboard) 
=> deactivate_user 
    - requirement (login_required, current_user)
    - templates (dashboard)
    - return template (index, login, sign-up)
"""


# Dashboard Page Routing
@blueprint.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    user = User.query.get_or_404(current_user.id)

    # To get all articles that are published and not deleted (from users).
    articles = db.session.query(Article).\
        filter(Article.author_id == current_user.id, Article.is_deleted == False).\
        order_by(Article.date_posted.desc()).all()

    # To get the counts of comments and likes for all articles.
    comment_likes_cnts = db.session\
        .query(Article.id.label("article_id"),
               func.count(Comment.comment).label("comments_count"),
               func.count(ArticleLike.user_id).label("likes_count")) \
        .outerjoin(Comment, Comment.article_id == Article.id) \
        .outerjoin(ArticleLike, ArticleLike.article_id == Article.id) \
        .group_by(Article.id).all()

    form = SearchForm()

    context = {
        "user": user,
        "articles": articles,
        "comment_likes_cnts": comment_likes_cnts,
        "form": form,
    }

    return render_template("dashboard.html", **context)


# Update User Profile Page Routing (done)
@blueprint.route("/update", methods=["GET", "POST"])
@login_required
def update():
    form = UserForm()
    user = User.query.get_or_404(current_user.id)

    if request.method == "POST" and current_user.is_authenticated:
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.bio = form.bio.data

        # Check for profile pic
        if request.files['profile_pic']:
            upload_image()

        try:
            db.session.commit()
            flash(f"User Profile updated successfully")
            return redirect(url_for("user.dashboard"))
        except:
            flash("Something went wrong. Please try again...")
            return redirect(url_for("user.update_user"))

    # only the author can edit his article
    if current_user.id == user.id:
        form.firstname.data = user.firstname
        form.lastname.data = user.lastname
        form.bio.data = user.bio

    else:
        flash(f"You are not authorized to update this user profile!")
        return redirect(url_for("user.dashboard"))

    context = {
        "form": form,
        "user": user,
    }

    return render_template("update-user.html", **context)


# DEACTIVATE USER PROFILE Route (done)
@blueprint.route("/deactivate", methods=["GET", "POST"])
@login_required
def deactivate():
    user = User.query.get_or_404(current_user.id)

    if current_user.is_authenticated:
        user.is_active = False
        try:
            db.session.commit()

            logout_user()
            flash(f"User: '{user.username}' deactivated successfully and will be deleted after 30 days, if not reactivated! \n To reactivate, use Contact Page to contact Admin.")
            return redirect(url_for("general.index"))
        except:
            logout_user()
            flash("Whoops! Something went wrong! Please try again...!")
            return redirect(url_for("auth.login"))
    else:
        flash(f"You are not authorized to deactivate this User: '{user.username}'")
        return redirect(url_for("general.index"))


# SEARCH MY ARTICLE ROUTE
@blueprint.route("/article/search", methods=["POST"])
@login_required
def article_search():
    form = SearchForm()
    word = form.search_word.data

    if form.validate_on_submit():
        search_word = word

        search_results = Article.query.\
            filter(Article.content.contains(search_word), Article.author_id == current_user.id).all()

        context = {
            "form": form,
            "search_word": search_word,
            "search_results": search_results
        }

        return render_template("search.html", **context)
