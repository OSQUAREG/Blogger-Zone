from flask import render_template, redirect, url_for, flash, Blueprint, request
from flask_login import login_required, current_user
from sqlalchemy import func, or_
from app.models import db, User, Article, Comment, ArticleLike
from app.utils import paginate_query
from app.webforms import SearchForm

blueprint = Blueprint("admin", __name__, template_folder="templates")


# ADMIN DASHBOARD ROUTE
@blueprint.route("/", methods=["GET", "POST"])
@blueprint.route("/article-search/<word>", methods=["GET", "POST"])
@login_required
def admin(word=None):
    users = db.session.query(User)
    articles = db.session.query(Article)

    # To get the counts of comments and likes for all articles.
    comment_likes_cnts = db.session. \
        query(Article.id.label("article_id"),
               func.count(Comment.comment).label("comments_count"),
               func.count(ArticleLike.user_id).label("likes_count")). \
        outerjoin(Comment, Comment.article_id == Article.id). \
        outerjoin(ArticleLike, ArticleLike.article_id == Article.id). \
        group_by(Article.id).all()

    # pagination
    users, next_page_users, prev_page_users = paginate_query(users, "admin.admin")
    articles, next_page_articles, prev_page_articles = paginate_query(articles, "admin.admin")

    # using the Article Search form to filter
    form = SearchForm()

    if request.method == "POST" and form.validate_on_submit():
        search_word = form.search_word.data

        print(search_word)

        articles = db.session.query(Article). \
            filter(Article.title.contains(search_word)). \
            order_by(Article.id)

        articles, next_page_articles, prev_page_articles = paginate_query(articles, "admin.admin")

        articles_context = {
            "search_word": search_word,
            "articles": articles,
            "next_page_articles": next_page_articles,
            "prev_page_articles": prev_page_articles,
        }

        return redirect(url_for("admin.admin", **articles_context))

    context = {
        "users": users,
        "articles": articles,
        "comment_likes_cnts": comment_likes_cnts,
        "next_page_users": next_page_users,
        "prev_page_users": prev_page_users,
        "next_page_articles": next_page_articles,
        "prev_page_articles": prev_page_articles,
        "form": form,
    }

    if current_user.is_authenticated and current_user.is_admin:
        return render_template("admin.html", **context)
    else:
        flash(f"You are not an admin!")
        return redirect(url_for("user.dashboard"))


# # ADMIN SEARCH USERS ROUTE
# @blueprint.route("/user-search", methods=["GET", "POST"])
# @blueprint.route("/user-search/<word>", methods=["GET", "POST"])
# @login_required
# def user_search(word=None):
#     form = SearchForm()
#
#     if not word:
#         search_word = form.search_word.data
#     else:
#         search_word = word
#
#     search_results = not db.session.query(User). \
#         filter(or_(User.firstname.contains(search_word),
#                    User.lastname.contains(search_word),
#                    User.email.contains(search_word),
#                    )). \
#         order_by(User.id)
#
#     search_results, next_page, prev_page = paginate_query(search_results, "admin.user-search")
#
#     context = {
#         "form": form,
#         "search_word": search_word,
#         "search_results": search_results,
#         "next_page": next_page,
#         "prev_page": prev_page,
#     }
#
#     return redirect(url_for("admin.admin", **context))
#
#
# # ADMIN SEARCH ARTICLES ROUTE
# @blueprint.route("/article-search", methods=["GET", "POST"])
# @blueprint.route("/article-search/<word>", methods=["GET", "POST"])
# @login_required
# def article_search(word=None):
#     form = SearchForm()
#
#     if not word:
#         search_word = form.search_word.data
#     else:
#         search_word = word
#
#     search_results = not db.session.query(User). \
#         filter(or_(User.firstname.contains(search_word),
#                    User.lastname.contains(search_word),
#                    User.email.contains(search_word),
#                    )). \
#         order_by(User.id)
#
#     search_results, next_page, prev_page = paginate_query(search_results, "admin.user-search")
#
#     context = {
#         "form": form,
#         "search_word": search_word,
#         "search_results": search_results,
#         "next_page": next_page,
#         "prev_page": prev_page,
#     }
#
#     return redirect(url_for("admin.admin", **context))
