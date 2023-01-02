from sqlalchemy import func
from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required, logout_user, current_user
from app.models import db, User, Article, Comment
from app.webforms import UserForm

blueprint = Blueprint("role", __name__, template_folder="templates")


# Create User Role
@blueprint.route("/user/delete/<int:id>", methods=["GET", "POST"])
@login_required
def create_role(id):
    user = User.query.get_or_404(id)
    pass
