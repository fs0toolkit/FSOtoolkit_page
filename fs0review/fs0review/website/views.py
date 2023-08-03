from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        # Get the form data
        review_summary = request.form.get('reviewSummaryInput')
        manager_input = request.form.get('managerinput')
        ralead4g_input = request.form.get('ralead4ginput')
        ralead5g_input = request.form.get('ralead5ginput')
        fs1ta_input = request.form.get('fs1tainput')
        guardian_input = request.form.get('guardianinput')
        architect_input = request.form.get('architectinput')
        other_input = request.form.get('otherinput')
        fst_input = request.form.get('fstinput')
        apo_input = request.form.get('apoinput')
        optional_input = request.form.get('optionalinput')
        comp1_input = request.form.get('Comp1')
        comp2_input = request.form.get('Comp2')
        comp3_input = request.form.get('Comp3')
        comp4_input = request.form.get('Comp4')
        comp5_input = request.form.get('Comp5')
        comp6_input = request.form.get('Comp6')
        comp7_input = request.form.get('Comp7')

        # Process the form data (you can store this data in a database)
        # For demonstration purposes, we'll just print the data
        print("Review Summary:", review_summary)
        print("Manager Input:", manager_input)
        print("RA Lead(4G) Input:", ralead4g_input)
        print("RA Lead(5G) Input:", ralead5g_input)
        print("FS1TA Input:", fs1ta_input)
        print("Guardian Input:", guardian_input)
        print("System Architect Input:", architect_input)
        print("Other Mandatory Input:", other_input)
        print("FST Input:", fst_input)
        print("APO Input:", apo_input)
        print("Other Optional Input:", optional_input)
        print("Comp1 Input:", comp1_input)
        print("Comp2 Input:", comp2_input)
        print("Comp3 Input:", comp3_input)
        print("Comp4 Input:", comp4_input)
        print("Comp5 Input:", comp5_input)
        print("Comp6 Input:", comp6_input)
        print("Comp7 Input:", comp7_input)

        # Redirect to the comment page after processing the form
        return redirect(url_for('views.comment'))

    return render_template("reviewtool.html", user=current_user)

@views.route('/check_review', methods=['GET', 'POST'])
def check_review():
    # Perform any necessary logic here
    # For example, get the review comments from the database
    # You can define the 'review_comments' variable here or retrieve it from somewhere else.

    # Then, render the comments.html template and pass any data if needed
    return render_template('comments.html', comments=review_comments)
