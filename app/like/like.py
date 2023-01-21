from flask import  redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from app.models import db, Article, ArticleLike

blueprint = Blueprint("like", __name__, template_folder="templates")


# ADD LIKE TO ARTICLE
@blueprint.route("/add/<int:id>", methods=["GET", "POST"])
@login_required
def add(id):
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
                return redirect(url_for("article.view", id=article.id))
        else:
            return redirect(url_for("article.view", id=article.id))


# REMOVE LIKE FROM ARTICLE
@blueprint.route("/remove/<int:id>", methods=["GET", "POST"])
@login_required
def delete(id):
    article = Article.query.get_or_404(id)
    like_exist = db.session.query(ArticleLike).filter(ArticleLike.article_id == id, ArticleLike.user_id == current_user.id).first()

    if current_user.is_authenticated:
        if like_exist:
            try:
                db.session.delete(like_exist)
                db.session.commit()
                return redirect(url_for("article.view", id=article.id))
            except:
                flash("Whoops! Something went wrong! Please try again...!")
                return redirect(url_for("article.view", id=article.id))
