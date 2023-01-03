from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User, Article
from app.webforms import UserForm
# from datetime import timedelta

blueprint = Blueprint("admin-users", __name__, template_folder="templates")


# MAKE ADMIN
@blueprint.route("/", methods=["GET"])
@login_required
def admin():
    users = db.session.query(User).all()
    articles = db.session.query(Article).all()

    context = {
        "users": users,
        "articles": articles,
    }

    if current_user.is_authenticated and current_user.is_admin:
        return render_template("admin.html", **context)
    else:
        flash(f"You are not an admin!")
        return redirect(url_for("user.dashboard"))


# MAKE ADMIN
@blueprint.route("/make-admin/<int:id>", methods=["GET", "POST"])
@login_required
def make_admin(id):
    user = User.query.get_or_404(id)

    if current_user.is_authenticated and current_user.is_admin:
        user.is_admin = True

        try:
            db.session.commit()
            flash(f"User: '{user.username}' is now an admin.")
            return redirect(url_for("admin-users.admin"))
        except:
            flash(f"Whoops! Something went wrong. Please try again!")
            return redirect(url_for("admin-users.admin"))


# REMOVE ADMIN
@blueprint.route("/remove-admin/<int:id>", methods=["GET", "POST"])
@login_required
def remove_admin(id):
    user = User.query.get_or_404(id)

    if current_user.is_authenticated and current_user.is_admin:
        user.is_admin = False

        try:
            db.session.commit()
            flash(f"User: '{user.username}' is removed from admin.")
            return redirect(url_for("admin-users.admin"))
        except:
            flash(f"Whoops! Something went wrong. Please try again!")
            return redirect(url_for("admin-users.admin"))


# DELETE USER
@blueprint.route("/delete-user/<int:id>", methods=["GET", "POST"])
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)

    if current_user.is_authenticated and current_user.is_admin:
        try:
            db.sessoin.delete(user)
            db.session.commit()
            flash(f"User: '{user.username}' is deleted successfully.")
            return redirect(url_for("admin-users.admin"))
        except:
            flash(f"Whoops! Something went wrong. Please try again!")
            return redirect(url_for("admin-users.admin"))


# DEACTIVATE USER
@blueprint.route("/deactivate-user/<int:id>", methods=["GET", "POST"])
@login_required
def deactivate_user(id):
    user = User.query.get_or_404(id)

    if current_user.is_authenticated and current_user.is_admin:
        user.is_active = False
        try:
            db.session.commit()
            flash(f"User: '{user.username}' is deactivated successfully.")
            return redirect(url_for("admin-users.admin"))
        except:
            flash(f"Whoops! Something went wrong. Please try again!")
            return redirect(url_for("admin-users.admin"))


# ACTIVATE USER
@blueprint.route("/activate-user/<int:id>", methods=["GET", "POST"])
@login_required
def activate_user(id):
    user = User.query.get_or_404(id)

    if current_user.is_authenticated and current_user.is_admin:
        user.is_active = True
        try:
            db.session.commit()
            flash(f"User: '{user.username}' is activated successfully.")
            return redirect(url_for("admin-users.admin"))
        except:
            flash(f"Whoops! Something went wrong. Please try again!")
            return redirect(url_for("admin-users.admin"))


# UPDATE USER
@blueprint.route("/update-user/<int:id>", methods=["GET", "POST"])
@login_required
def update_user(id):
    form = UserForm()
    user = User.query.get_or_404(id)

    if request.method == "POST" and current_user.id == user.id and current_user.is_admin:
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

    # only the user or admin can edit this user profile
    if current_user.id == user.id or current_user.is_admin:
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
