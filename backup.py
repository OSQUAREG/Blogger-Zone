from models import app, db, User, Article, Message, Comment
from forms import UserForm, LoginForm, ArticleForm, MessageForm, CommentForm
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, LoginManager, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# setting up login manager
login_manager = LoginManager(app)
# login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))


# Home Page Routing (done)
@app.route("/")
def index():
    articles = Article.query.order_by(Article.date_posted.desc()).all
    authors = User.query.order_by(User.id).all
    if current_user.is_authenticated:
        firstname = current_user.firstname
        context = {"firstname" : firstname}
    context = {
        "articles" : articles,
        "authors" : authors
        }    
    return render_template("index.html", **context)


# About Page Routing (done)
@app.route("/about")
def about():
    authors = User.query.order_by(User.id).all
    return render_template("about.html", authors=authors)


# Sign Up Routing (done)
@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    form = UserForm()

    if request.method == "POST":
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


# Create Article Page Routing
@app.route("/create-article", methods=["GET", "POST"])
@login_required
def create_article():
    form = ArticleForm()
    if request.method == "POST":
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            slug = form.slug.data
            is_draft = form.is_draft.data
            author = current_user.id # for the author foreign key link
            # adding new article to the db
            new_article = Article(
                title=title, content=content, slug=slug, is_draft=is_draft,author_id=author
            )
            db.session.add(new_article)
            db.session.commit()
            # checking if is_draft is active
            if is_draft:
                flash(f"Article titled: '{title}' Saved As Draft successfully")
            else:
                flash(f"Article titled: '{title}' Published successfully")
        
            return redirect(url_for("dashboard"))
        return redirect(url_for("dashboard"))
    return render_template("create-article.html", form=form)


# View Single Published Article Page Routing
@app.route("/article/view/<int:id>", methods=["GET","POST"])
def view_article(id):    
    article = Article.query.get_or_404(id)
    form = CommentForm()
    comments = Comment.query.order_by(Comment.date_added.desc()).all
    
    if not article.is_draft:     
        return render_template("view-article.html", article=article, form=form, comments=comments)
    else:
        flash(f"This Article is a draft! You can only edit it.")
        return redirect(url_for("dashboard"))



# Edit Article Page Routing
@app.route("/article/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_article(id):
    form = ArticleForm()
    article = Article.query.get_or_404(id)

    if form.validate_on_submit():
        if current_user.id == article.author_id:
            article.title = form.title.data
            article.slug = form.slug.data
            article.content = form.content.data
            try:
                db.session.add(article)
                db.session.commit()
                flash(f"Article titled: '{article.title}' updated successfully")
                return redirect(url_for("view_article", id=article.id))
            except:
                flash("Something went wrong. Please try again...")
                return redirect(url_for("edit_article", id=article.id))
    \
    # only the author can edit his article
    if current_user.id == article.author_id:
        form.title.data = article.title
        form.slug.data = article.slug
        form.content.data = article.content
    else:
        flash(f"You are not authorized to edit this article!")
        return redirect(url_for("view_article", article.id))
    return render_template("edit-article.html", form=form, article=article)


# Delete Article Routing (done)
@app.route("/article/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_article(id):
    article = Article.query.get_or_404(id)

    if current_user.id == article.author_id:
        try:
            # deleting from the DB
            db.session.delete(article)
            db.session.commit()
            
            flash(f"Article: '{article.title}' Deleted Successfully!")
            articles = Article.query.order_by(Article.date_posted.desc()).all
            return redirect(url_for("dashboard", articles=articles))

        except:
            flash("Whoops! Something went wrong! Please try again...!")
            articles = Article.query.order_by(Article.date_posted.desc()).all
            return redirect(url_for("view_article", id=article.id))
    else:
        flash(f"You are not authorized to delete the Article: '{article.title}'")
        return redirect(url_for("view_article", id=article.id))


# Add Comment Routing (done)
@app.route("/article/add-comment/<int:id>", methods=["GET","POST"])
@login_required
def add_comment(id):
    article = Article.query.get_or_404(id)
    form = CommentForm()
    comments = Comment.query.order_by(Comment.date_added.desc()).all

    if request.method == "POST":
        comment = form.comment.data
        commenter = current_user.id

        comment = Comment(comment=comment, user_id=commenter, article_id=article.id)
        db.session.add(comment)
        db.session.commit()

        # resetting/clearing the form
        # comment = ""
        flash(f"Comment added successfully")
        return redirect(url_for("view_article", id=article.id, form=form, comments=comments))
    else:
        flash(f"Whoops! Something went wrong. Please try again...")
        return redirect(url_for("view_article", id=article.id, form=form, comments=comments))


# Contact Page Routing (done)
@app.route("/contact", methods=["GET","POST"])
def message():
    form = MessageForm()

    if request.method == "POST":
        name = form.name.data
        email = form.email.data
        message = form.message.data

        # adding new article to the db
        contact = Message(
            name=name, email=email, message=message
        )
        db.session.add(contact)
        db.session.commit()

        # resetting/clearing the form
        name = ""
        email = ""
        message = ""
        flash(f"Message sent successfully")
        return redirect(url_for("index"))
    else:
        flash(f"Whoops! Something went wrong. Please try again...")
    return render_template("contact.html", form=form)
    


if __name__ == "__main__":
    app.run(debug=True)
