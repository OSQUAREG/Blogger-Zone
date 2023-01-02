from app.webforms import MessageForm
from flask import render_template, request, redirect, url_for, flash, Blueprint
from app.models import db, Article, User, Message, Comment
from flask_login import current_user
from sqlalchemy import func

blueprint = Blueprint("general", __name__, template_folder="templates")

"""
GENERAL Routes:
=> index : login not required DONE
=> about : login not required DONE
=> message : login not required DONE
"""


# Home Page Routing (done)
@blueprint.route("/")
def index():
    articles = db.session.query(Article).\
        filter(Article.is_draft == False).\
        order_by(Article.date_posted.desc()).all()

    authors = db.session.query(User).order_by(User.id).all

    comments = db.session.query(Article.id.label("article_id"), func.count(Comment.comment).label("count")).\
        outerjoin(Comment, Comment.article_id == Article.id).\
        group_by(Article.id).all()

    context = {
        "articles": articles,
        "authors": authors,
        "comments": comments
    }

    return render_template("index.html", **context)


# About Page Routing (done)
@blueprint.route("/about")
def about():
    authors = User.query.order_by(User.id).all
    context = {
        "authors": authors
    }
    return render_template("about.html", **context)


# Contact Page Routing (done)
@blueprint.route("/contact", methods=["GET", "POST"])
def message():
    form = MessageForm()

    if request.method == "POST":
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            message = form.message.data

            # adding new article to the db
            contact = Message(
                name=name, email=email, message=message
            )
            db.session.add(contact)
            db.session.commit()

            flash(f"Message sent successfully")
            return redirect(url_for("general.message"))
        else:
            flash(f"Whoops! Something went wrong. Please try again...")

    context = {
        "form": form,
    }

    return render_template("contact.html", **context)
