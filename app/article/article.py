from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from sqlalchemy import func
from app.models import db, Article, Comment, ArticleLike
from app.utils import paginate_query
from app.webforms import ArticleForm, CommentForm

blueprint = Blueprint("article", __name__, template_folder="templates")

"""
ARTICLE Routes:
=> create_article : COMPLETE
    - required (form.data, form)
    - templates (base, create-article, dashboard)
=> view_article : COMPLETE
    - required (id)
    - templates (base, view-article, dashboard)
=> delete-article : COMPLETE
    - required (login_required, current_user)
    - templates (base, login, dashboard)
"""


# CREATE ARTICLE ROUTE
@blueprint.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = ArticleForm()
    
    if request.method == "POST" and form.validate_on_submit():
        title = form.title.data  # gets title data from form title field
        content = form.content.data  # gets content data from form content field
        is_draft = form.is_draft.data
        author = current_user.id  # for the author foreign key link

        # creating a new instance of Article and adding it to db
        new_article = Article(title=title, content=content, is_draft=is_draft, author_id=author, last_updated_on=None)

        # adding slug to published articles
        if not new_article.is_draft:
            new_article.slug = new_article.slugify_title

        db.session.add(new_article)
        db.session.commit()

        # checking if is_draft is active
        if is_draft:
            flash(f"Article titled: '{title}' Saved As Draft successfully")
        else:
            flash(f"Article titled: '{title}' Published successfully")

        return redirect(url_for("article.view", id=new_article.id, slug=new_article.slug))

    context = {
        "form": form,
    }

    return render_template("create-article.html", **context)


# VIEW SINGLE ARTICLE ROUTE
@blueprint.route("/view/<int:id>/<slug>", methods=["GET", "POST"])
def view(id: int, slug):
    form = CommentForm()
    article = Article.query.get_or_404(id)

    # To get all comments for current article.
    comments = Comment.query\
        .filter(Comment.article_id == article.id)\
        .order_by(Comment.date_added.desc())

    # pagination
    comments, next_page, prev_page = paginate_query(comments, "article.view")

    # To count the comments for current article.
    comment_cnts = db.session.query(func.count(Comment.comment).label("count"))\
        .filter(Comment.article_id == article.id)\
        .all()
    comment_count = comment_cnts[0][0]

    # To count the likes for current article.
    article_likes_cnts = db.session.query(func.count(ArticleLike.user_id).label("count"))\
        .filter(ArticleLike.article_id == article.id)\
        .all()
    article_likes_count = article_likes_cnts[0][0]

    # To check if user has liked the current article.
    user_article_like = db.session.query(ArticleLike)\
        .filter(ArticleLike.article_id == article.id)\
        .all()

    context = {
        "form": form,
        "article": article,
        "comments": comments,
        "comment_count": comment_count,
        "article_likes_count": article_likes_count,
        "user_article_like": user_article_like,
        "next_page": next_page,
        "prev_page": prev_page,
        }

    if not article.is_draft:
        return render_template("view-article.html", **context)
    else:
        return redirect(url_for("user.dashboard"))


# EDIT ARTICLE ROUTE
@blueprint.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    form = ArticleForm()
    article = Article.query.get_or_404(id)

    # to update and save the edited article to database
    if form.validate_on_submit() and current_user.id == article.author_id:
        article.title = form.title.data
        article.content = form.content.data
        article.is_draft = form.is_draft
        article.last_updated_by = current_user.username

        if form.is_draft.data:
            article.is_draft = True
            article.slug = None
            flash(f"Article titled: '{article.title}' updated and saved successfully")
        else:
            article.is_draft = False
            article.slug = article.slugify_title
            flash(f"Article titled: '{article.title}' updated and published successfully")
        try:
            db.session.commit()
            return redirect(url_for("article.view", id=article.id))
        except:
            flash("Something went wrong. Please try again...")
            return redirect(url_for("article.edit", id=article.id))

    # only the author can edit his own article
    if current_user.id == article.author_id:
        # to initially fill up the update form with existing data from database
        form.title.data = article.title
        form.content.data = article.content
        form.is_draft.data = article.is_draft
    else:
        flash(f"You are not authorized to edit this article!")
        return redirect(url_for("article.view", id=article.id))

    context = {
        "form": form,
        "article": article,
    }

    return render_template("edit-article.html", **context)


# # DELETE ARTICLE ROUTE
# @blueprint.route("/delete/<int:id>", methods=["GET", "POST"])
# @login_required
# def delete(id):
#     article = Article.query.get_or_404(id)
#
#     if current_user.id == article.author_id:
#         try:
#             # deleting from the DB
#             db.session.delete(article)
#             db.session.commit()
#
#             flash(f"Article: '{article.title}' Deleted Successfully!")
#             return redirect(url_for("user.dashboard"))
#         except:
#             flash("Whoops! Something went wrong! Please try again...!")
#             return redirect(url_for("article.view", id=article.id))
#     else:
#         flash(f"You are not authorized to delete the Article: '{article.title}'")
#         return redirect(url_for("article.view", id=article.id))


# PUBLISH ARTICLE ROUTE
@blueprint.route("/publish/<int:id>", methods=["GET", "POST"])
@login_required
def publish(id):
    article = Article.query.get_or_404(id)

    if current_user.id == article.author_id:
        article.is_draft = False
        article.slug = article.slugify_title

        try:
            db.session.commit()
            flash(f"Article: '{article.title}' is now published.")
            return redirect(url_for("user.dashboard"))
        except:
            flash(f"Whoops! Something went wrong. Please try again!")
            return redirect(url_for("user.dashboard"))


# UNPUBLISH ARTICLE ROUTE
@blueprint.route("/unpublish/<int:id>", methods=["GET", "POST"])
@login_required
def unpublish(id):
    article = Article.query.get_or_404(id)

    if current_user.id == article.author_id:
        article.is_draft = True
        article.slug = None

        try:
            db.session.commit()
            flash(f"Article: '{article.title}' is now unpublished.")
            return redirect(url_for("user.dashboard"))
        except:
            flash(f"Whoops! Something went wrong. Please try again!")
            return redirect(url_for("user.dashboard"))


# REMOVE ARTICLE FROM USER
@blueprint.route("/remove/<int:id>", methods=["GET", "POST"])
@login_required
def remove(id):
    article = Article.query.get_or_404(id)

    if current_user.id == article.author_id:
        article.is_deleted = True
        article.slug = None

        try:
            db.session.commit()
            flash(f"Article: '{article.title}' is deleted from user's articles successfully.")
            return redirect(url_for("user.dashboard"))
        except:
            flash(f"Whoops! Something went wrong. Please try again!")
            return redirect(url_for("user.dashboard"))
