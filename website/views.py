from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from .models import User, Review, Comment
from . import db
from flask import Flask, render_template, request
import pymysql
from datetime import datetime 
views = Blueprint('views', __name__)

def sql_connector():
    conn = pymysql.connect(user='root', password='asdf1234', db='fs0tool', host='127.0.0.1', port=13306)
    c = conn.cursor()
    return conn, c

# Route for the signup page
@views.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Check if the email already exists in the database
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists. Please choose another.', category='error')
        elif password1 != password2:
            flash('Passwords do not match. Please try again.', category='error')
        else:
            # Create a new user and add them to the database
            new_user = User(email=email, first_name=first_name, password=password1)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully. You can now log in.', category='success')
            return redirect(url_for('views.login'))

    return render_template('signup.html')

# Route for the login page
@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user, remember=True)
            flash('Login successful!', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('Login failed. Please check your email and password.', category='error')

    return render_template('login.html')

# Route for the home page (requires login)
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        # Capture form data
        review_type = request.form.get('review_type')
        title = request.form.get('Titleinput')
        owner = current_user.email  # Use the email of the logged-in user
        category = request.form.get('review_type2')
        sol_area = request.form.get('review_type3')
        req_area = request.form.get('review_type4')
        release_label = request.form.get('review_type5')
        rat = request.form.get('review_type6')
        review_start_date = request.form.get('review_start_date')
        if review_start_date:
            try:
        # Attempt to parse the date
                parsed_dates = datetime.strptime(review_start_date, '%Y-%m-%d')
        # If the parsing succeeds, it's a valid date
            except ValueError:
        # If parsing fails, it's not a valid date
                flash('Invalid date format for review_start_date', category='error')
        review_end_date = request.form.get('review_end_date')
        if review_end_date:
            try:
        # Attempt to parse the date
                parsed_datee = datetime.strptime(review_end_date, '%Y-%m-%d')
        # If the parsing succeeds, it's a valid date
            except ValueError:
        # If parsing fails, it's not a valid date
                flash('Invalid date format for review_end_date', category='error')

        
        
        primary_tm = request.form.get('primaryTMInput')
        sign_off = request.form.get('review_type7')
        review_summary = request.form.get('reviewSummaryInput')

        conn, c = sql_connector()
            # Insert form data into the 'reviews' table
        c.execute("""
                INSERT INTO reviews (
                    review_type, title, owner, category, sol_area, req_area,
                    release_label, rat,review_start_date, review_end_date,
                    primary_tm, sign_off, review_summary
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                review_type, title, owner, category, sol_area, req_area,
                release_label, rat, parsed_dates, parsed_datee,
                primary_tm, sign_off, review_summary
            ))
        conn.commit()
        flash('Review added!', category='success')

    return render_template('home.html', user=current_user)

# Route for the comment page (requires login)
@views.route('/comment', methods=['GET', 'POST'])
@login_required
def comment():
    if request.method == 'POST':
        comment_text = request.form.get('comment-input')  # Change to match your HTML input name

        if comment_text:  # Check if comment_text is not empty

            flash('Comment added!', category='success')
        else:
            flash('Comment cannot be empty!', category='error')

    # Fetch data from the 'reviews' table for display on the comment page
    reviews = Review.query.all()

    return render_template('comment.html', user=current_user, reviews=reviews)


# Route for logging out (requires login)
@views.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect(url_for('views.login'))




