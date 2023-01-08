from flask import render_template, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from sqlalchemy import func
from app.models import db, User, Article, Comment, ArticleLike
from app.utils import paginate_query

blueprint = Blueprint("admin", __name__, template_folder="templates")


# ADMIN DASHBOARD ROUTE
@blueprint.route("/", methods=["GET"])
@login_required
def admin():
    users = db.session.query(User)
    articles = db.session.query(Article)

    # To get the counts of comments and likes for all articles.
    comment_likes_cnts = db.session \
        .query(Article.id.label("article_id"),
               func.count(Comment.comment).label("comments_count"),
               func.count(ArticleLike.user_id).label("likes_count")) \
        .outerjoin(Comment, Comment.article_id == Article.id) \
        .outerjoin(ArticleLike, ArticleLike.article_id == Article.id) \
        .group_by(Article.id).all()

    # pagination
    users, next_page_users, prev_page_users = paginate_query(users, "admin.admin")
    articles, next_page_articles, prev_page_articles = paginate_query(articles, "admin.admin")

    for page in articles.iter_pages():
        print(page)

    context = {
        "users": users,
        "articles": articles,
        "comment_likes_cnts": comment_likes_cnts,
        "next_page_users": next_page_users,
        "prev_page_users": prev_page_users,
        "next_page_articles": next_page_articles,
        "prev_page_articles": next_page_articles,
    }

    if current_user.is_authenticated and current_user.is_admin:
        return render_template("admin.html", **context)
    else:
        flash(f"You are not an admin!")
        return redirect(url_for("user.dashboard"))

