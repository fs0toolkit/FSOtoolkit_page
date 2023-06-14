# views.py

from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', category='error')
            return render_template("home.html", user=current_user)

    # Get the user's email
    email = current_user.email

    # Example feature details
    feature_details = [
        {
            'feature': 'Review type',
            'value': 'New Review',
            'mandatory_reviewer': 'Technical Manager',
            'mandatory_reviewer_email': 'xyz@nokia.com',
            'mandatory_review_status': 'Reviewed'
        },
        {
            'feature': 'Title',
            'value': 'P01: Review tool online',
            'mandatory_reviewer': 'RA Lead (4G)',
            'mandatory_reviewer_email': 'xyz@nokia.com',
            'mandatory_review_status': 'Reviewed'
        },
        {
            'feature': 'Owner',
            'value': email,  # User's email as the owner
            'mandatory_reviewer': 'RA Lead (5G)',
            'mandatory_reviewer_email': 'xyz@nokia.com',
            'mandatory_review_status': 'Reviewed'
        },
        # Add more feature details here...
    ]

    return render_template("home.html", user=current_user, feature_details=feature_details)
