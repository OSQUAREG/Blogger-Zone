from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User, Article
from app.webforms import UserForm
# from datetime import timedelta

blueprint = Blueprint("admin", __name__, template_folder="templates")


# MAKE ADMIN
@blueprint.route("/admin", methods=["GET"])
@login_required
def admin():
    check_user = User.query.get_or_404(current_user.id)
    users = db.session.query(User).all()
    articles = db.session.query(Article).all()

    context = {
        "users": users,
        "articles": articles,
        "check_user": check_user
    }

    if check_user.is_admin:
        print(check_user.is_admin)
        print("User is admin")
        return render_template("admin.html", **context)
    else:
        flash(f"You are not an admin!")
        return redirect(url_for("user.dashboard"))


    # else:
    #     try:
    #         flash(f"You are not an admin!")
    #         redirect(url_for("user.dashboard", id=current_user.id))
    #     except:
    #         flash(f"Whoops! Something went wrong. Please try again!")
    #         redirect(url_for("user.dashboard", id=current_user.id))


# MAKE ADMIN
@blueprint.route("/admin/make-admin/<int:id>", methods=["GET", "POST"])
@login_required
def make_admin(id):
    user = User.query.get_or_404(id)
    is_admin = User.query.filter(User.is_admin == current_user.is_admin, User.username == "admin")

    if current_user.is_authenticated and is_admin:
        user.is_admin = True

        try:
            db.session.commit()
            flash(f"User: '{user.username}' is now an admin.")
            return redirect(url_for("admin.admin"))
        except:
            flash(f"Whoops! Something went wrong. Please try again!")
            return redirect(url_for("admin.admin"))


# REMOVE ADMIN
@blueprint.route("/admin/remove-admin/<int:id>", methods=["GET", "POST"])
@login_required
def remove_admin(id):
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


# MAKE ADMIN
@blueprint.route("/admin/delete-user/<int:id>", methods=["GET", "POST"])
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)

    if current_user.is_authenticated:
        user.is_admin = False

        try:
            db.session.commit()
            flash(f"User: '{user.username}' is removed from admin.")
            return redirect(url_for("admin.admin"))
        except:
            flash(f"Whoops! Something went wrong. Please try again!")
