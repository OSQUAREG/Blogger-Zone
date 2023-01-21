from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, login_required, logout_user, current_user, confirm_login
from sqlalchemy.sql import or_
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User
from app.webforms import UserForm, LoginForm, PasswordForm

blueprint = Blueprint("auth", __name__, template_folder="templates")

"""
AUTH Routes:
=> sign_up : COMPLETE
    - required (user_data)
    - templates (base, sign-up, login, about)
=> log_in : COMPLETE
    - required (login_required)
    - templates (base, login, sign-up)
=> log_out : COMPLETE
    - required (login_required, current_user)
    - templates (base, login, dashboard)
"""


# SIGN UP ROUTE
@blueprint.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    form = UserForm()

    if request.method == "POST" and form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        bio = form.bio.data

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
            user = User(firstname=firstname, lastname=lastname, username=username, email=email, password_hash=password_hash, bio=bio, is_admin=bool(0))
            # adding to the db
            db.session.add(user)
            db.session.commit()

            flash(f"Account signed up successfully!")
            return redirect(url_for("auth.login"))

    context = {
        "form": form,
    }

    return render_template("sign-up.html", title="Sign Up", **context)


# LOGIN ROUTE
@blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == "POST" and form.validate_on_submit:
        username_email = form.username_email.data
        password = form.password.data

        # checking if username or email exist
        user_exists = User.query.filter(or_(User.username == username_email, User.email == username_email)).first()

        if user_exists:
            if user_exists.is_active:
                if check_password_hash(user_exists.password_hash, password):
                    login_user(user_exists)
                    flash("Login Successful")
                    return redirect(url_for("general.index"))
                else:
                    flash("Wrong Password! Please try again...")
                    return redirect(url_for("auth.login"))

            else:
                flash("Your account has been deactivated! Please go to 'Contact' page to contact Admin!")
        else:
            flash("User does not exist! Please try again...or Sign up.")
            return redirect(url_for("auth.login"))

    context = {
        "form": form
    }

    return render_template("login.html", title="Login", **context)


# LOGOUT ROUTE
@blueprint.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for("auth.login"))


# # RE-AUTHENTICATE ROUTE
# @blueprint.route("/confirm", methods=["GET", "POST"])
# def confirm():
#     form = LoginForm()
#
#     if request.method == "POST" and form.validate_on_submit():
#         password = form.password.data
#
#         if check_password_hash(current_user.password_hash, password):
#             confirm_login()
#             flash(u"User re-authenticated!")
#             # return redirect(request.args.get("next") or url_for("general.index"))
#         else:
#             flash("Password incorrect!")
#
#     return render_template("re-auth.html")


# CHANGE PASSWORD ROUTE
@blueprint.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = PasswordForm()

    if request.method == "POST" and form.validate_on_submit() and current_user.is_authenticated:
        old_password = form.old_password.data
        new_password = form.new_password.data
        confirm_new_password = form.confirm_new_password

        user = User.query.filter_by(email=current_user.email)
        user_to_update = user.first()

        if user_to_update.is_active:
            if old_password != new_password:
                # checks old password_hash
                if check_password_hash(user_to_update.password_hash, old_password):
                    # hash the new password
                    new_pwd_hash = generate_password_hash(new_password)
                    # update user password
                    user.update(dict(password_hash=new_pwd_hash))
                    # save/commit changes
                    db.session.commit()
                    # logs out user
                    logout_user()

                    flash("Password changed successfully! Please login again...")
                    return redirect(url_for("auth.login"))
                else:
                    flash("Wrong Old Password! Please try again...")
                    return redirect(url_for("auth.change_password"))
            else:
                flash("New password should be different from the old password!")
                return redirect(url_for("auth.change_password"))
        else:
            flash("Your account is deactivated! Please contact admin in 'Contact' page.")
            return redirect(url_for("auth.change_password"))

    return render_template("change-password.html", title="Change Password", form=form)
