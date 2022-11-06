from models import app, db, Article, Comment
from forms import ArticleForm, CommentForm
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user


# Create Article Page Routing
@app.route("/create-article", methods=["GET", "POST"])
@login_required
def create_article():
    form = ArticleForm()
    if request.method == "POST":
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            slug = form.slug.data
            is_draft = form.is_draft.data
            author = current_user.id # for the author foreign key link
            # adding new article to the db
            new_article = Article(
                title=title, content=content, slug=slug, is_draft=is_draft,author_id=author
            )
            db.session.add(new_article)
            db.session.commit()
            # checking if is_draft is active
            if is_draft:
                flash(f"Article titled: '{title}' Saved As Draft successfully")
            else:
                flash(f"Article titled: '{title}' Published successfully")
        
            return redirect(url_for("dashboard"))
        return redirect(url_for("dashboard"))
    return render_template("create-article.html", form=form)


# View Single Published Article Page Routing
@app.route("/article/view/<int:id>", methods=["GET","POST"])
def view_article(id):    
    article = Article.query.get_or_404(id)
    form = CommentForm()
    comments = Comment.query.order_by(Comment.date_added.desc()).all
    
    if article.is_draft == False:     
        return render_template("view-article.html", article=article, form=form, comments=comments)
    else:
        return redirect(url_for("dashboard"))



# Edit Article Page Routing
@app.route("/article/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_article(id):
    form = ArticleForm()
    article = Article.query.get_or_404(id)

    if form.validate_on_submit():
        if current_user.id == article.author_id:
            article.title = form.title.data
            article.slug = form.slug.data
            article.content = form.content.data
            article.is_draft = form.is_draft

            if form.is_draft.data == True:
                article.is_draft = True
                flash(f"Article titled: '{article.title}' updated and saved successfully")
            else:
                article.is_draft = False
                flash(f"Article titled: '{article.title}' updated and published successfully")
            try:
                db.session.add(article)
                db.session.commit()
                return redirect(url_for("view_article", id=article.id))
            except:
                flash("Something went wrong. Please try again...")
                return redirect(url_for("edit_article", id=article.id))
    \
    # only the author can edit his article
    if current_user.id == article.author_id:
        form.title.data = article.title
        form.slug.data = article.slug
        form.content.data = article.content
        form.is_draft.data = article.is_draft
    else:
        flash(f"You are not authorized to edit this article!")
        return redirect(url_for("view_article", article.id))
    return render_template("edit-article.html", form=form, article=article)


# Delete Article Routing (done)
@app.route("/article/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_article(id):
    article = Article.query.get_or_404(id)

    if current_user.id == article.author_id:
        try:
            # deleting from the DB
            db.session.delete(article)
            db.session.commit()
            
            flash(f"Article: '{article.title}' Deleted Successfully!")
            articles = Article.query.order_by(Article.date_posted.desc()).all
            return redirect(url_for("dashboard", articles=articles))

        except:
            flash("Whoops! Something went wrong! Please try again...!")
            articles = Article.query.order_by(Article.date_posted.desc()).all
            return redirect(url_for("view_article", id=article.id))
    else:
        flash(f"You are not authorized to delete the Article: '{article.title}'")
        return redirect(url_for("view_article", id=article.id))


# Add Comment Routing (done)
@app.route("/article/add-comment/<int:id>", methods=["GET","POST"])
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

        # resetting/clearing the form
        # comment = ""
        flash(f"Comment added successfully")
        return redirect(url_for("view_article", id=article.id, form=form, comments=comments))
    else:
        flash(f"Whoops! Something went wrong. Please try again...")
        return redirect(url_for("view_article", id=article.id, form=form, comments=comments))
