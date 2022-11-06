from models import app, db, User, Article
from forms import UserForm, LoginForm
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, LoginManager, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# setting up login manager
login_manager = LoginManager(app)
# login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))


# Sign Up Routing (done)
@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    form = UserForm()

    if request.method == "POST":
        if form.validate_on_submit():
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
                return redirect(url_for("sign_up"))
            elif email_exists:
                flash(f"Whoops!!! Email '{email}' already exist! Please try again...")
                return redirect(url_for("sign_up"))
            # confirming passwords match
            elif password != confirm_password:
                flash(f"Whoops!!! Passwords do not match! Please try again...")
            else:
                # hashing the password
                password_hash = generate_password_hash(password)
                # creating an instance of user
                user = User(firstname=firstname, lastname=lastname, username=username, email=email, password_hash=password_hash, about_author=about_author, is_admin=bool(0))
                # adding to the db
                db.session.add(user)
                db.session.commit()

                flash(f"Account signed up successfully!")
                return redirect(url_for("login"))
    return render_template("sign-up.html", form=form)


# Login Page Routing (done)
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit:
            username_email = form.username_email.data
            password = form.password.data

            user_exists = User.query.filter_by(username=username_email).first()
            email_exists = User.query.filter_by(email=username_email).first()

            if user_exists or email_exists:
                if user_exists:
                    if check_password_hash(user_exists.password_hash, password):
                        login_user(user_exists)
                        flash("Login Successful")
                        return redirect(url_for("dashboard"))
                    else:
                        password = ""
                        flash("Wrong Password! Please try again...")
                elif email_exists:
                    if check_password_hash(email_exists.password_hash, password):
                        login_user(email_exists)
                        flash("Login Successful")
                        return redirect(url_for("dashboard"))
                    else:
                        password = ""
                        flash("Wrong Password! Please try again...")
                else:
                    password = ""
                    flash("Wrong Password! Please try again...")
                    return redirect(url_for("login"))
            else:
                username_email = ""
                flash("Wrong Username or Email! Please try again...")
                return redirect(url_for("login"))
    return render_template("login.html", form=form)


# Logout Routing (done)
@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("You have been Logged Out!")
    return redirect(url_for("login"))


# Dashboard Page Routing
@app.route("/dashboard")
@login_required
def dashboard():
    id = current_user.id    
    user = User.query.get_or_404(id)
    articles = Article.query.order_by(Article.date_posted.desc()).all
    context = {
        "id" : id,
        "user" : user, 
        "articles" : articles
    }
    return render_template("dashboard.html", **context)


# Edit User Profile Page Routing (done)
@app.route("/user/update/<int:id>", methods=["GET", "POST"])
@login_required
def update_user(id):
    form = UserForm()
    user = User.query.get_or_404(id)

    if request.method == "POST":
        if current_user.id == user.id:
            user.firstname = form.firstname.data
            user.lastname = form.lastname.data
            user.about_author = form.about_author.data

            try:
                db.session.commit()
                flash(f"User Profile updated successfully")
                return redirect(url_for("dashboard", id=user.id))
            except:
                flash("Something went wrong. Please try again...")
                return redirect(url_for("edit_article", id=user.id))
    \
    # only the author can edit his article
    if current_user.id == user.id:
        form.firstname.data = user.firstname
        form.lastname.data = user.lastname
        form.about_author.data = user.about_author
    else:
        flash(f"You are not authorized to edit this article!")
        return redirect(url_for("view_article", user.id))
    return render_template("update-user.html", form=form, user=user)


# Delete User Profile Routing (done)
@app.route("/user/delete/<int:id>", methods=["GET", "POST"])
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
                return redirect(url_for("sign_up"))
            else:
                flash(f"User: '{user.username}' deleted successfully!")
        except:
            flash("Whoops! Something went wrong! Please try again...!")
            articles = Article.query.order_by(Article.date_posted.desc()).all
            return redirect(url_for("sign_up"))
    else:
        flash(f"You are not authorized to delete this User: '{user.username}'")
        return redirect(url_for("index", articles=articles))

