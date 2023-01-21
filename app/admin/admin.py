from flask import render_template, redirect, url_for, flash, Blueprint, request
from flask_login import login_required, current_user
from sqlalchemy import func, or_, desc, distinct
from app.models import db, User, Article, Comment, ArticleLike
from app.utils import paginate_query
from app import sett
from app.webforms import SearchForm

blueprint = Blueprint("admin", __name__, template_folder="templates")


# ADMIN DASHBOARD ROUTE
@blueprint.route("/", methods=["GET", "POST"])
@login_required
def admin():
    users = db.session.query(User)
    articles = db.session.query(Article)

    # pagination
    users, next_page_users, prev_page_users, user_page = paginate_query(users, "admin.admin", "user_page")
    articles, next_page_articles, prev_page_articles, article_page = paginate_query(articles, "admin.admin", "article_page")

    # To get the counts of comments and likes for all articles.
    comment_likes_cnts = db.session. \
        query(Article.id.label("article_id"),
              func.count(Comment.comment).label("comments_count"),
              func.count(distinct(ArticleLike.user_id)).label("likes_count")). \
        outerjoin(Comment, Comment.article_id == Article.id). \
        outerjoin(ArticleLike, ArticleLike.article_id == Article.id). \
        group_by(Article.id).all()

    print(comment_likes_cnts)

    context = {
        "users": users,
        "articles": articles,
        "comment_likes_cnts": comment_likes_cnts,
        "next_page_users": next_page_users,
        "prev_page_users": prev_page_users,
        "next_page_articles": next_page_articles,
        "prev_page_articles": prev_page_articles,
        "user_page": user_page,
        "article_page": article_page,
    }

    if current_user.is_authenticated and current_user.is_admin:
        return render_template("admin.html", title="Admin Dashboard", **context)
    else:
        flash(f"You are not an admin!")
        return redirect(url_for("user.dashboard"))


# # ADMIN DASHBOARD ROUTE
# @blueprint.route("/", methods=["GET", "POST"])
# @blueprint.route("/<search_w>", methods=["GET", "POST"])
# @blueprint.route("/<search_w>/<search_u>", methods=["GET", "POST"])
# @login_required
# def admin(search_w=None, search_u=None):
#     # Filter Code
#     form = SearchForm()
#
#     if not search_w:
#         search_user = form.search_word.data
#     else:
#         search_user = search_w
#
#     if not search_w:
#         search_word = form.search_word.data
#     else:
#         search_word = search_w
#
#     articles = db.session.query(Article). \
#         filter(or_(Article.content.contains(search_word),
#                    Article.title.contains(search_word)
#                    )). \
#         order_by(desc(Article.date_posted))
#
#     # pagination with search
#     users, next_page_users, prev_page_users, user_page = paginate_query(users, "admin.admin", "user_page", search=search_u)
#     articles, next_page_articles, prev_page_articles, article_page = paginate_query(articles, "admin.admin", "article_page", search=search_w)
#
#     # users = db.session.query(User)
#     # articles = db.session.query(Article)
#
#     # pagination
#     users, next_page_users, prev_page_users, user_page = paginate_query(users, "admin.admin", "user_page")
#     articles, next_page_articles, prev_page_articles, article_page = paginate_query(articles, "admin.admin", "article_page")
#
#     # To get the counts of comments and likes for all articles.
#     comment_likes_cnts = db.session. \
#         query(Article.id.label("article_id"),
#               func.count(Comment.comment).label("comments_count"),
#               func.count(ArticleLike.user_id).label("likes_count")). \
#         outerjoin(Comment, Comment.article_id == Article.id). \
#         outerjoin(ArticleLike, ArticleLike.article_id == Article.id). \
#         group_by(Article.id).all()
#
#     context = {
#         "users": users,
#         "articles": articles,
#         "comment_likes_cnts": comment_likes_cnts,
#         "next_page_users": next_page_users,
#         "prev_page_users": prev_page_users,
#         "next_page_articles": next_page_articles,
#         "prev_page_articles": prev_page_articles,
#         "user_page": user_page,
#         "article_page": article_page,
#         "form": form,
#         "search_user": search_user,
#         "search_word": search_word,
#     }
#
#     if current_user.is_authenticated and current_user.is_admin:
#         return render_template("admin.html", **context)
#     else:
#         flash(f"You are not an admin!")
#         return redirect(url_for("user.dashboard"))
