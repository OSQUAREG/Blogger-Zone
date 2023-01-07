from flask import request, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from app.models import db, Article, Comment
from app.webforms import CommentForm

blueprint = Blueprint("comment", __name__, template_folder="templates")


# ADD COMMENT ROUTE
@blueprint.route("/add/<int:id>/add-comment", methods=["GET", "POST"])
@login_required
def add(id):
    article = Article.query.get_or_404(id)
    form = CommentForm()

    if request.method == "POST":
        comment = form.comment.data
        commenter = current_user.id

        comment = Comment(comment=comment, user_id=commenter, article_id=article.id)
        db.session.add(comment)
        db.session.commit()

        flash(f"Comment added successfully")
        return redirect(url_for("article.view_article", id=article.id))
    else:
        flash(f"Whoops! Something went wrong. Please try again...")
        return redirect(url_for("article.view_article", id=article.id))


# DELETE COMMENT ROUTE
@blueprint.route("/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete(id):
    comment = Comment.query.get_or_404(id)

    if current_user.id == comment.user_id or current_user.is_admin:
        try:
            # deleting from the DB
            db.session.delete(comment)
            db.session.commit()

            return redirect(url_for("article.view_article", id=comment.article_id))
        except:
            flash("Whoops! Something went wrong! Please try again...!")
            return redirect(url_for("article.view_article", id=comment.article_id))
    else:
        return redirect(url_for("article.view_article", id=comment.article_id))
