from app.webforms import MessageForm, SearchForm
from flask import render_template, request, redirect, url_for, flash, Blueprint
from app.models import db, Article, User, Message, Comment, ArticleLike
from sqlalchemy import func, desc

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

    # To get top 5 authors with the highest number of published article.
    top_authors = db.session.query(User.firstname, User.lastname, User.id, func.count(Article.id).label("articles_count")).\
        outerjoin(Article, Article.author_id == User.id).\
        filter(Article.is_draft == False,
               Article.is_deleted == False,
               User.is_active == True,
               User.username != "admin",
               "articles_count" is not None).\
        group_by(User.id).\
        order_by(desc("articles_count")).limit(5).all()

    # To get top 10 articles with the highest number of likes.
    top_articles = db.session.query(Article.title, Article.id, func.count(ArticleLike.user_id).label("likes_count")).\
        outerjoin(ArticleLike, ArticleLike.article_id == Article.id).\
        filter(Article.is_draft == False,
               Article.is_deleted == False,
               "likes_count" is not None).\
        group_by(Article.id).\
        order_by(desc("likes_count")).limit(10).all()

    # To get all articles that are published and not deleted.
    articles = db.session.query(Article)\
        .filter(Article.is_draft == False, Article.is_deleted == False)\
        .order_by(Article.date_posted.desc()).all()

    # To get the counts of comments and likes for all articles.
    comment_likes_cnts = db.session \
        .query(Article.id.label("article_id"),
               func.count(Comment.comment).label("comments_count"),
               func.count(ArticleLike.user_id).label("likes_count")) \
        .outerjoin(Comment, Comment.article_id == Article.id) \
        .outerjoin(ArticleLike, ArticleLike.article_id == Article.id) \
        .group_by(Article.id).all()

    form = SearchForm()

    context = {
        "articles": articles,
        "top_authors": top_authors,
        "top_articles": top_articles,
        "comment_likes_cnts": comment_likes_cnts,
        "form": form,
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


# SEARCH ROUTE
@blueprint.route("/search", methods=["POST"])
def search():
    form = SearchForm()
    word = form.search_word.data

    if form.validate_on_submit():
        search_word = word

        search_results = Article.query.filter(Article.content.contains(search_word)).all()

        context = {
            "form": form,
            "search_word": search_word,
            "search_results": search_results
        }

        return render_template("search.html", **context)


# VIEW AUTHOR PROFILE
@blueprint.route("/author/<int:id>", methods=["GET"])
def author(id):
    user = User.query.get_or_404(id)

    user_details = db.session.query(User, User.id, func.count(Article.id).label("articles_count")). \
        outerjoin(Article, Article.author_id == User.id). \
        filter(user.id == Article.author_id, Article.is_draft is False, Article.is_deleted is False,
               User.is_active is True,
               User.username != "admin").first()

    user_articles = Article.query.\
        filter(Article.author_id == user.id, Article.is_draft == False, Article.is_deleted is False).\
        all()

    comment_likes_cnts = db.session. \
        query(Article.id.label("article_id"),
               func.count(Comment.comment).label("comments_count"),
               func.count(ArticleLike.user_id).label("likes_count")). \
        filter(Article.author_id == user.id, Article.is_draft is False, Article.is_deleted is False). \
        outerjoin(Comment, Comment.article_id == Article.id).\
        outerjoin(ArticleLike, ArticleLike.article_id == Article.id).\
        group_by(Article.id).all()

    context = {
        "user": user,
        "user_details": user_details,
        "user_articles": user_articles,
        "comment_likes_cnts": comment_likes_cnts
    }

    return render_template("author.html", **context)
