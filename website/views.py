from flask import (
    Blueprint, render_template, request, flash, redirect, url_for, Flask
)
from flask_login import login_required, login_user, logout_user, current_user
from .models import User, Review, Comment
from . import db
from datetime import datetime
import re
import requests
import adal
from flask_mysqldb import MySQL
import yaml
import pymysql
from flask import current_app
from flask_mysqldb import MySQL


views = Blueprint('views', __name__)




# Define your Office 365 API endpoint and version
api_endpoint = "https://outlook.office365.com/api/v2.0/me/sendmail"

# Define your Azure AD settings
tenant_id = "YOUR_TENANT_ID"
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
resource = "https://outlook.office365.com/"



def sql_connector():
    conn = pymysql.connect(user='root', password='asdf1234', db='fs0tool', host='127.0.0.1', port=13306)
    c = conn.cursor()
    return conn, c



# Route for the home page (requires login)
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        print("inside teh ")
        if 'ResetButton' in request.form:
            print("ResetButton")
            try:
                review_start_date = datetime.strptime(request.form.get('review_start_date'), '%Y-%m-%d')
                review_end_date = datetime.strptime(request.form.get('review_end_date'), '%Y-%m-%d')
            except ValueError:
                flash('Invalid date format for review_start_date or review_end_date', category='error')
                return redirect(url_for('views.home'))

            # Get other form data and insert into the database (using parameterized queries)
            review_type = request.form.get('review_type')
            title = request.form.get('Titleinput')
            owner = current_user.email
            category = request.form.get('review_type2')
            sol_area = request.form.get('dropdown3')
            req_area = request.form.get('review_type4')
            release_label = request.form.get('review_type5')
            rat = request.form.get('review_type6')
            primary_tm = request.form.get('primaryTMInput')
            sign_off = request.form.get('review_type7')
            review_summary = request.form.get('reviewSummaryInput')

            conn, cur = sql_connector()
            # cur =  MySQL.connection.cursor()
            cur.execute("""
                INSERT INTO reviews (
                    review_type, title, owner, category, sol_area, req_area,
                    release_label, rat, review_start_date, review_end_date,
                    primary_tm, sign_off, review_summary
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                review_type, title, owner, category, sol_area, req_area,
                release_label, rat, review_start_date, review_end_date,
                primary_tm, sign_off, review_summary
            ))
            conn.commit()
            flash('Review added!', category='success')



            
        elif 'EmailButton' in request.form:
            print("in draft email")
                        # Get the owner's email from the logged-in user
            owner = current_user.email  # Replace this with your actual method of getting the owner's email
            
            # Get the primary_tm email from the form
            primary_tm = request.form.get('primaryTMInput')
            
            # Authenticate with Azure AD to get an access token
            authority_url = f"https://login.microsoftonline.com/{tenant_id}"
            context = adal.AuthenticationContext(authority_url)
            token = context.acquire_token_with_client_credentials(
                resource,
                client_id,
                client_secret
            )

            # Create a draft email
            headers = {
                "Authorization": f"Bearer {token['access_token']}",
                "Content-Type": "application/json",
            }

            email_data = {
                "Message": {
                    "Subject": "Your Email Subject",
                    "Body": {
                        "ContentType": "Text",
                        "Content": "Your email content here."
                    },
                    "ToRecipients": [
                        {
                            "EmailAddress": {
                                "Address": primary_tm  # Use the primary_tm email as the recipient
                            }
                        }
                    ],
                    "From": {
                        "EmailAddress": {
                            "Address": owner  # Use the owner's email as the sender
                        }
                    }
                },
                "SaveToSentItems": "false"
            }

            response = requests.post(api_endpoint, json=email_data, headers=headers)

            if response.status_code == 201:
                return "Draft email created successfully."
            else:
                return "Error creating draft email. Status code:", response.status_code


        elif 'UpdateButton' in request.form:

            num = 0
            print("Jai shreeram")
            
            # Capture form data for retrieving an existing record
            category = request.form.get('review_type2')
            sol_area = request.form.get('dropdown3')
            req_area = request.form.get('review_type4')
            
            print(sol_area, req_area, category)
            
            conn, c = sql_connector()
            
            # Retrieve a record from the 'reviews' table based on the combination of criteria
            c.execute("""
                SELECT *
                FROM reviews
                WHERE sol_area = %s AND req_area = %s AND category = %s
            """, (sol_area, req_area, category))
            
            record = c.fetchone()
            print("helolegbvsghsergwago1 \n")
            print(record)
            
            if record:
                # Unpack the record, assuming it has the expected number of values
                num, review_type, title, owner, _, _, _, release_label, rat, review_start_date, review_end_date, primary_tm, sign_off, review_summary = record
                
                flash('Record found!', category='success')
            else:
                flash('No record found for the specified criteria.', category='error')
            
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




