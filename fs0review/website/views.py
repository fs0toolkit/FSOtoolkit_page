from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Comment, Review
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        comment = request.form.get('comment')  # Gets the comment from the HTML

        new_review = Review(data=comment, user_id=current_user.id)  # Providing the schema for the comment
        db.session.add(new_review)  # Adding the comment to the database
        db.session.commit()
        flash('Comment added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/comment', methods=['POST'])
@login_required
def comment():
    if request.method == 'POST': 
        comment_text = request.form.get('comment')  # Gets the comment from the HTML

        new_comment = Comment(data=comment_text, user_id=current_user.id)  # Providing the schema for the comment
        db.session.add(new_comment)  # Adding the comment to the database
        db.session.commit()
        flash('Comment added!', category='success')

    return render_template("home.html", user=current_user)
