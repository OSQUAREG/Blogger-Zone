from sqlalchemy.sql import and_

from app.webforms import MessageForm
from flask import render_template, request, redirect, url_for, flash, Blueprint
from app.models import db, Article, User, Message, Comment, ArticleLike
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
@blueprint.route("/", methods=["GET"])
def index():
    authors = db.session.query(User).order_by(User.id).all

    # To get all articles that are published and not deleted.
    articles = db.session.query(Article).\
        filter(Article.is_draft == False, Article.is_deleted == False).\
        order_by(Article.date_posted.desc()).all()

    # To get the counts of comments and likes for all articles.
    comment_likes_cnts = db.session \
        .query(Article.id.label("article_id"),
               func.count(Comment.comment).label("comments_count"),
               func.count(ArticleLike.user_id).label("likes_count")) \
        .outerjoin(Comment, Comment.article_id == Article.id) \
        .outerjoin(ArticleLike, ArticleLike.article_id == Article.id) \
        .group_by(Article.id).all()

    context = {
        "articles": articles,
        "authors": authors,
        "comment_likes_cnts": comment_likes_cnts,
    }

    return render_template("index.html", **context)


# About Page Routing (done)
@blueprint.route("/about", methods=["GET"])
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
