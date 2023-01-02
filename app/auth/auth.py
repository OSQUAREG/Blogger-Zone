from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User
from app.webforms import UserForm, LoginForm

# from datetime import timedelta

blueprint = Blueprint("auth", __name__, template_folder="templates")

"""
AUTH Routes:
=> sign_up : COMPLETE
    - required (user_data)
    - templates (base, sign-up, login)
=> log_in : COMPLETE
    - required (login_required)
    - templates (base, login, sign-up)
=> log_out : COMPLETE
    - required (login_required, current_user)
    - templates (base, login, dashboard)
"""


# Sign Up Routing (done)
@blueprint.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    form = UserForm()
    check_user = User.query.get_or_404(current_user.id)

    if request.method == "POST" and form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        about_author = form.about_author.data

        # checking if username and email already exists
        user_exists = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first()

        if user_exists:
            flash(f"Whoops!!! Username '{username}' already exist! Please try again...")
            return redirect(url_for("auth.sign_up"))
        elif email_exists:
            flash(f"Whoops!!! Email '{email}' already exist! Please try again...")
            return redirect(url_for("auth.sign_up"))
        # confirming passwords match
        elif password != confirm_password:
            flash(f"Whoops!!! Passwords do not match! Please try again...")
        else:
            # hashing the password
            password_hash = generate_password_hash(password)

            # creating an instance of user
            user = User(firstname=firstname, lastname=lastname, username=username, mail=email, password_hash=password_hash, about_author=about_author, is_admin=bool(0))
            # adding to the db
            db.session.add(user)
            db.session.commit()

            flash(f"Account signed up successfully!")
            return redirect(url_for("auth.login"))

    context = {
        "form": form,
        "check_user": check_user
    }

    return render_template("sign-up.html", **context)


# Login Page Routing (done)
@blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    check_user = User.query.get_or_404(current_user.id)

    if request.method == "POST" and form.validate_on_submit:
        username_email = form.username_email.data
        password = form.password.data

        user_exists = User.query.filter_by(username=username_email).first()
        email_exists = User.query.filter_by(email=username_email).first()

        if user_exists or email_exists:
            if user_exists:
                if check_password_hash(user_exists.password_hash, password):
                    login_user(user_exists)  # duration=timedelta(minutes=1))
                    flash("Login Successful")
                    return redirect(url_for("user.dashboard"))
                else:
                    flash("Wrong Password! Please try again...")

            elif email_exists:
                if check_password_hash(email_exists.password_hash, password):
                    login_user(email_exists)  # duration=timedelta(minutes=1))
                    flash("Login Successful")
                    return redirect(url_for("user.dashboard"))
                else:
                    flash("Wrong Password! Please try again...")

            else:
                flash("Wrong Password! Please try again...")
                return redirect(url_for("auth.login"))

        else:
            flash("Wrong Username or Email! Please try again...")
            return redirect(url_for("auth.login"))

    context = {
        "form": form,
        "check_user": check_user
    }

    return render_template("login.html", **context)


# Logout Routing (done)
@blueprint.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("You have been Logged Out!")
    return redirect(url_for("auth.login"))
