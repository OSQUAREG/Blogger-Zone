import os
import uuid
from flask import request, flash, redirect, url_for
from flask_login import current_user
from werkzeug.utils import secure_filename

from app import settings
from app.models import User, db


def upload_image():
    from app.main import app

    user = User.query.get_or_404(current_user.id)
    user.profile_pic = request.files['profile_pic']

    # Get and secure image name (to avoid code injection)
    secure_image_name = secure_filename(user.profile_pic.filename)
    unique_image_name = str(uuid.uuid1()) + "_" + secure_image_name  # add uuid to make unique.
    saved_image = request.files['profile_pic']  # save the image
    user.profile_pic = unique_image_name  # save to db

    try:
        db.session.commit()
        saved_image.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_image_name))
        flash(f"User Profile Picture uploaded successfully")
        return redirect(url_for("user.dashboard"))
    except:
        flash("Something went wrong. Please try uploading again...")
        return redirect(url_for("user.update_user"))


def paginate_query(query, url_for_func: str):
    # per_page is from the settings in config file further defined from .env file
    # url_for is the url for the next_page and prev_page button.

    # defining page and per_page param.
    page = request.args.get("page", default=1, type=int)
    per_page = int(settings.per_page)

    # paginating the query result
    paginated = query.paginate(per_page=per_page, page=page, error_out=True)

    # defining next page and previous page routes
    next_page = url_for(url_for_func, page=paginated.next_num) \
        if paginated.has_next else None
    prev_page = url_for(url_for_func, page=paginated.prev_num) \
        if paginated.has_prev else None

    return paginated, next_page, prev_page

