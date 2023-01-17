from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from sqlalchemy import func
from werkzeug.security import generate_password_hash

from app.models import db, User, Article, Comment, ArticleLike
from app.webforms import UserForm
# from datetime import timedelta

blueprint = Blueprint("admin-users", __name__, template_folder="templates")

#
# # ADMIN DASHBOARD ROUTE
# @admin.route("/", methods=["GET"])
# @login_required
# def admin():
#     users = db.session.query(User).all()
#     articles = db.session.query(Article).all()
#
#     # To get the counts of comments and likes for all articles.
#     comment_likes_cnts = db.session \
#         .query(Article.id.label("article_id"),
#                func.count(Comment.comment).label("comments_count"),
#                func.count(ArticleLike.user_id).label("likes_count")) \
#         .outerjoin(Comment, Comment.article_id == Article.id) \
#         .outerjoin(ArticleLike, ArticleLike.article_id == Article.id) \
#         .group_by(Article.id).all()
#
#     context = {
#         "users": users,
#         "articles": articles,
#         "comment_likes_cnts": comment_likes_cnts
#     }
#
#     if current_user.is_authenticated and current_user.is_admin:
#         return render_template("admin.html", **context)
#     else:
#         flash(f"You are not an admin!")
#         return redirect(url_for("user.dashboard"))
#

# MAKE ADMIN
@blueprint.route("/promote/<int:id>", methods=["GET", "POST"])
@login_required
def promote(id):
    user = User.query.get_or_404(id)

    if current_user.is_authenticated and current_user.is_admin:
        user.is_admin = True

        try:
            db.session.commit()
            flash(f"User: '{user.username}' is now an admin.")
            return redirect(url_for("admin.admin"))
        except:
            flash(f"Whoops! Something went wrong. Please try again!")
            return redirect(url_for("admin.admin"))


# REMOVE ADMIN
@blueprint.route("/demote/<int:id>", methods=["GET", "POST"])
@login_required
def demote(id):
    user = User.query.get_or_404(id)

    if current_user.is_authenticated and current_user.is_admin:
        user.is_admin = False

        try:
            db.session.commit()
            flash(f"User: '{user.username}' is removed from admin.")
            return redirect(url_for("admin.admin"))
        except:
            flash(f"Whoops! Something went wrong. Please try again!")
            return redirect(url_for("admin.admin"))


# DELETE USER
@blueprint.route("/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete(id):
    user = User.query.get_or_404(id)

    if current_user.is_authenticated and current_user.is_admin:
        try:
            db.session.delete(user)
            db.session.commit()
            flash(f"User: '{user.username}' is deleted successfully.")
            return redirect(url_for("admin.admin"))
        except:
            flash(f"Whoops! Something went wrong. Please try again!")
            return redirect(url_for("admin.admin"))


# DEACTIVATE USER
@blueprint.route("/deactivate/<int:id>", methods=["GET", "POST"])
@login_required
def deactivate(id):
    user = User.query.get_or_404(id)

    if current_user.is_authenticated and current_user.is_admin:
        user.is_active = False
        try:
            db.session.commit()
            flash(f"User: '{user.username}' is deactivated successfully.")
            return redirect(url_for("admin.admin"))
        except:
            flash(f"Whoops! Something went wrong. Please try again!")
            return redirect(url_for("admin.admin"))


# ACTIVATE USER
@blueprint.route("/activate/<int:id>", methods=["GET", "POST"])
@login_required
def activate(id):
    user = User.query.get_or_404(id)

    if current_user.is_authenticated and current_user.is_admin:
        user.is_active = True
        try:
            db.session.commit()
            flash(f"User: '{user.username}' is activated successfully.")
            return redirect(url_for("admin.admin"))
        except:
            flash(f"Whoops! Something went wrong. Please try again!")
            return redirect(url_for("admin.admin"))


# UPDATE USER
@blueprint.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update(id):
    form = UserForm()
    user = User.query.get_or_404(id)

    if request.method == "POST" and current_user.is_admin:
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.bio = form.bio.data

        try:
            db.session.commit()
            flash(f"User Profile updated successfully")
            return redirect(url_for("admin.admin", id=user.id))
        except:
            flash("Something went wrong. Please try again...")
            return redirect(url_for("admin-users.update", id=user.id))

    # only admin can edit this user profile via this route
    if current_user.is_admin:
        form.firstname.data = user.firstname
        form.lastname.data = user.lastname
        form.bio.data = user.bio
    else:
        flash(f"You are not authorized to update this user profile!")
        return redirect(url_for("user.dashboard", id=user.id))

    context = {
        "form": form,
        "user": user,
    }

    return render_template("admin-update-user.html", **context)


# VIEW USER PROFILE
@blueprint.route("/view/<int:id>", methods=["GET"])
@login_required
def view(id):
    user = User.query.get_or_404(id)
    user_articles = Article.query.filter(Article.author_id == user.id).all()

    comment_likes_cnts = db.session \
        .query(Article.id.label("article_id"),
               func.count(Comment.comment).label("comments_count"),
               func.count(ArticleLike.user_id).label("likes_count")) \
        .outerjoin(Comment, Comment.article_id == Article.id) \
        .outerjoin(ArticleLike, ArticleLike.article_id == Article.id) \
        .group_by(Article.id).all()

    context = {
        "user": user,
        "user_articles": user_articles,
        "comment_likes_cnts": comment_likes_cnts
    }

    return render_template("admin-user-dashboard.html", **context)


# AUTO-RESET USER PASSWORD
@blueprint.route("/reset-password/<int:id>", methods=["GET", "POST"])
@login_required
def reset_password(id):
    # user = User.query.get_or_404(id)
    user = User.query.filter_by(id=id)
    user_to_reset = user.first()

    if current_user.is_authenticated and current_user.is_admin:
        # user = User.query.filter_by(email=user.email)

        # hash the new password
        new_pwd_hash = generate_password_hash("p@ssword123")
        # update user password
        user.update(dict(password_hash=new_pwd_hash))
        # save/commit changes
        db.session.commit()

        flash(f"User: {user_to_reset.username}'s Password changed successfully!")
        return redirect(url_for("admin.admin", id=user_to_reset.id))

