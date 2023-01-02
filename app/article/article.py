from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from sqlalchemy import func
from sqlalchemy.sql.elements import Null
from datetime import datetime
from app.models import db, Article, Comment, User
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


# Create Article Page Routing
@blueprint.route("/article/create", methods=["GET", "POST"])
@login_required
def create_article():
    form = ArticleForm()
    
    if request.method == "POST":
        if form.validate_on_submit(): 
            title = form.title.data
            content = form.content.data
            slug = form.slug.data
            is_draft = form.is_draft.data
            author = current_user.id  # for the author foreign key link

            # adding new article to the db
            new_article = Article(title=title, content=content, slug=slug, is_draft=is_draft, author_id=author, last_updated_on=None)

            db.session.add(new_article)
            db.session.commit()

            # checking if is_draft is active
            if is_draft:
                flash(f"Article titled: '{title}' Saved As Draft successfully")
            else:
                flash(f"Article titled: '{title}' Published successfully")

            return redirect(url_for("user.dashboard"))
        return redirect(url_for("user.dashboard"))

    context = {
        "form": form,
    }

    return render_template("create-article.html", **context)


# View Single Published Article Page Routing
@blueprint.route("/article/view/<int:id>", methods=["GET", "POST"])
def view_article(id):
    article = Article.query.get_or_404(id)
    form = CommentForm()
    comments = Comment.query.filter(Comment.article_id == article.id).order_by(Comment.date_added.desc()).all()

    counts = db.session.query(Article.id.label("article_id"), func.count(Comment.comment).label("count")). \
        outerjoin(Comment, Comment.article_id == Article.id). \
        group_by(Article.id).all()

    if not article.is_draft:
        context = {
            "article": article,
            "form": form,
            "comments": comments,
            "counts": counts,
            }
        return render_template("view-article.html", **context)
    else:
        return redirect(url_for("user.dashboard"))


# Edit Article Page Routing
@blueprint.route("/article/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_article(id):
    form = ArticleForm()
    article = Article.query.get_or_404(id)

    if form.validate_on_submit() and current_user.id == article.author_id:
        article.title = form.title.data
        article.slug = form.slug.data
        article.content = form.content.data
        article.is_draft = form.is_draft

        if form.is_draft.data:
            article.is_draft = True
            article.last_updated_on = datetime.utcnow
            flash(f"Article titled: '{article.title}' updated and saved successfully")
        else:
            article.is_draft = False
            article.last_updated_on = datetime.utcnow
            flash(f"Article titled: '{article.title}' updated and published successfully")
        try:
            db.session.add(article)
            db.session.commit()
            return redirect(url_for("article.view_article", id=article.id))
        except:
            flash("Something went wrong. Please try again...")
            return redirect(url_for("article.edit_article", id=article.id))

    # only the author can edit his own article
    if current_user.id == article.author_id:
        form.title.data = article.title
        form.slug.data = article.slug
        form.content.data = article.content
        form.is_draft.data = article.is_draft
    else:
        flash(f"You are not authorized to edit this article!")
        return redirect(url_for("article.view_article", article.id))

    context = {
        "form": form,
        "article": article,
    }

    return render_template("edit-article.html", **context)


# Delete Article Routing (done)
@blueprint.route("/article/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_article(id):
    article = Article.query.get_or_404(id)

    if current_user.id == article.author_id:
        try:
            # deleting from the DB
            db.session.delete(article)
            db.session.commit()

            flash(f"Article: '{article.title}' Deleted Successfully!")
            # articles = Article.query.order_by(Article.date_posted.desc()).all
            return redirect(url_for("user.dashboard"))
        except:
            flash("Whoops! Something went wrong! Please try again...!")
            return redirect(url_for("article.view_article", id=article.id))
    else:
        flash(f"You are not authorized to delete the Article: '{article.title}'")
        return redirect(url_for("article.view_article", id=article.id))


# Add Comment Routing (done)
@blueprint.route("/article/add-comment/<int:id>", methods=["GET", "POST"])
@login_required
def add_comment(id):
    article = Article.query.get_or_404(id)
    form = CommentForm()
    comments = Comment.query.order_by(Comment.date_added.desc()).all

    context = {
        "id": article.id,
        "form": form,
        "comments": comments
    }

    if request.method == "POST":
        comment = form.comment.data
        commenter = current_user.id

        comment = Comment(comment=comment, user_id=commenter, article_id=article.id)
        db.session.add(comment)
        db.session.commit()

        flash(f"Comment added successfully")
        return redirect(url_for("article.view_article", **context))
    else:
        flash(f"Whoops! Something went wrong. Please try again...")
        return redirect(url_for("article.view_article", **context))
