from sqlalchemy import func
from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required, logout_user, current_user
from app.models import db, User, Article, Comment, ArticleLike, CommentLike
from app.webforms import UserForm

blueprint = Blueprint("like", __name__, template_folder="templates")


# ADD LIKE TO ARTICLE
@blueprint.route("/like-article/<int:id>", methods=["GET", "POST"])
@login_required
def like_article(id):
    article = Article.query.get_or_404(id)
    like_exist = db.session.query(ArticleLike)\
        .filter(ArticleLike.article_id == id, ArticleLike.user_id == current_user.id)\
        .first()

    if current_user.is_authenticated:
        if like_exist is None:
            user_id = current_user.id
            article_id = article.id

            new_like = ArticleLike(user_id=user_id, article_id=article_id)
            try:
                db.session.add(new_like)
                db.session.commit()
                return redirect(url_for("article.view_article", id=article.id))
            except:
                flash("Whoops! Something went wrong! Please try again...!")
                return redirect(url_for("article.view_article", id=article.id))
        else:
            return redirect(url_for("article.view_article", id=article.id))


# REMOVE LIKE FROM ARTICLE
@blueprint.route("/unlike-article/<int:id>", methods=["GET", "POST"])
@login_required
def unlike_article(id):
    article = Article.query.get_or_404(id)
    like_exist = db.session.query(ArticleLike).filter(ArticleLike.article_id == id, ArticleLike.user_id == current_user.id).first()

    if current_user.is_authenticated:
        if like_exist:
            try:
                db.session.delete(like_exist)
                db.session.commit()
                return redirect(url_for("article.view_article", id=article.id))
            except:
                flash("Whoops! Something went wrong! Please try again...!")
                return redirect(url_for("article.view_article", id=article.id))


# ADD LIKE TO COMMENT
@blueprint.route("/<int:art_id>/like-comment/<int:com_id>", methods=["GET", "POST"])
@login_required
def like_comment(art_id, com_id):
    article = Article.query.get_or_404(art_id)
    comment = Comment.query.get_or_404(com_id)

    like_exist = db.session.query(CommentLike)\
        .filter(CommentLike.comment_id == comment.id, CommentLike.user_id == current_user.id)\
        .first()

    if current_user.is_authenticated:
        if like_exist is None:
            user_id = current_user.id
            comment_id = comment.id

            new_like = CommentLike(user_id=user_id, comment_id=comment_id)
            try:
                db.session.add(new_like)
                db.session.commit()
                return redirect(url_for("article.view_article", id=article.id))
            except:
                flash("Whoops! Something went wrong! Please try again...!")
                return redirect(url_for("article.view_article", id=article.id))
        else:
            return redirect(url_for("article.view_article", id=article.id))


# REMOVE LIKE FROM COMMENT
@blueprint.route("/unlike-comment/<int:id>", methods=["GET", "POST"])
@login_required
def unlike_comment(id):
    article = Article.query.get_or_404(id)
    like_exist = db.session.query(ArticleLike).filter(ArticleLike.article_id == id, ArticleLike.user_id == current_user.id).first()

    if current_user.is_authenticated:
        if like_exist:
            try:
                db.session.delete(like_exist)
                db.session.commit()
                return redirect(url_for("article.view_article", id=article.id))
            except:
                flash("Whoops! Something went wrong! Please try again...!")
                return redirect(url_for("article.view_article", id=article.id))

