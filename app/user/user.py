from sqlalchemy import func
from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required, logout_user, current_user
from app.models import db, User, Article, Comment
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
=> delete_user 
    - required (login_required, admin_user)
    - pages (admin)
=> deactivate_user 
    - required (login_required, current_user)
    - pages (dashboard)
"""


# Dashboard Page Routing
@blueprint.route("/dashboard")
@login_required
def dashboard():
    user = User.query.get_or_404(current_user.id)
    check_user = User.query.get_or_404(current_user.id)

    articles = db.session.query(Article).\
        filter(Article.author_id == current_user.id).\
        order_by(Article.date_posted.desc()).all()

    comments = db.session.query(Article.id.label("article_id"), func.count(Comment.comment).label("count")). \
        outerjoin(Comment, Comment.article_id == Article.id). \
        group_by(Article.id).all()

    context = {
        "user": user,
        "check_user": check_user,
        "articles": articles,
        "comments": comments
    }

    return render_template("dashboard.html", **context)


# Edit User Profile Page Routing (done)
@blueprint.route("/user/update/<int:id>", methods=["GET", "POST"])
@login_required
def update_user(id):
    form = UserForm()
    user = User.query.get_or_404(id)
    check_user = User.query.get_or_404(current_user.id)

    if request.method == "POST" and current_user.id == user.id:
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.about_author = form.about_author.data

        try:
            db.session.commit()
            flash(f"User Profile updated successfully")
            return redirect(url_for("dashboard", id=user.id))
        except:
            flash("Something went wrong. Please try again...")
            return redirect(url_for("update_user", id=user.id))

    # only the author can edit his article
    if current_user.id == user.id:
        form.firstname.data = user.firstname
        form.lastname.data = user.lastname
        form.about_author.data = user.about_author
    else:
        flash(f"You are not authorized to update this user profile!")
        return redirect(url_for("dashboard", id=user.id))

    context = {
        "form": form,
        "user": user,
        "check_user": check_user
    }

    return render_template("update-user.html", **context)


# Delete User Profile Routing (done)
@blueprint.route("/user/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)

    if current_user.id == user.id:
        try:
            # deleting from the DB
            db.session.delete(user)
            db.session.commit()

            if current_user.is_authenticated:
                logout_user()
                flash(f"User: '{user.username}' deleted successfully!")
                return redirect(url_for("auth.sign_up"))
            else:
                flash(f"User: '{user.username}' deleted successfully!")
        except:
            flash("Whoops! Something went wrong! Please try again...!")
            return redirect(url_for("auth.sign_up"))
    else:
        flash(f"You are not authorized to delete this User: '{user.username}'")
        articles = Article.query.order_by(Article.date_posted.desc()).all
        return redirect(url_for("general.index", articles=articles))


# Create User Role
@blueprint.route("/user/delete/<int:id>", methods=["GET", "POST"])
@login_required
def create_role(id):
    user = User.query.get_or_404(id)
    pass
