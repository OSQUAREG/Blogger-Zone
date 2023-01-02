from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from sqlalchemy.sql.elements import Null
from datetime import datetime
from app.models import db, Article, Comment
from app.webforms import CommentForm

blueprint = Blueprint("comment", __name__, template_folder="templates")


# Add Comment Routing (done)
@blueprint.route("/article/<int:id>/add-comment", methods=["GET", "POST"])
@login_required
def add_comment(id):
    article = Article.query.get_or_404(id)
    form = CommentForm()
    comments = Comment.query.order_by(Comment.date_added.desc()).all

    if request.method == "POST":
        comment = form.comment.data
        commenter = current_user.id

        comment = Comment(comment=comment, user_id=commenter, article_id=article.id)
        db.session.add(comment)
        db.session.commit()

        context = {
            "id": article.id,
            "form": form,
            "comments": comments
        }

        flash(f"Comment added successfully")
        return redirect(url_for("article.view_article", **context))
    else:
        flash(f"Whoops! Something went wrong. Please try again...")
        return redirect(url_for("article.view_article", **context))


# Edit Comment
@blueprint.route("/article/<int:article_id>/edit-comment/<int:comment_id>", methods=["GET", "POST"])
@login_required
def edit_comment(article_id, comment_id):
    pass


# Edit Comment
@blueprint.route("/article/<int:article_id>/delete-comment/<int:comment_id>", methods=["GET", "POST"])
@login_required
def delete_comment(id):
    pass
