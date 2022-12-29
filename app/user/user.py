from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User, Article
from app.webforms import UserForm, LoginForm

blueprint = Blueprint("user", __name__, template_folder="templates")


# Dashboard Page Routing
@blueprint.route("/dashboard")
@login_required
def dashboard():
    id = current_user.id    
    user = User.query.get_or_404(id)
    articles = Article.query.order_by(Article.date_posted.desc()).all
    context = {
        "id": id,
        "user": user,
        "articles": articles
    }
    return render_template("dashboard.html", **context)


# Edit User Profile Page Routing (done)
@blueprint.route("/user/update/<int:id>", methods=["GET", "POST"])
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
    return render_template("user.update-user.html", form=form, user=user)


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
