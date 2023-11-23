from flask import (
    Blueprint, render_template, request, flash, redirect, url_for, Flask, g
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
tenant_id = "f8cdef31-a31e-4b4a-93e4-5f571e91255a"
client_id = "a0e4b12a-5afa-4590-9a27-4763c8584c99"
client_secret = "IrV8Q~0TeSOk1NBC.jYHp.YM0sgIqWVsZKg7McSq"
resource = "https://outlook.office365.com/"



def sql_connector():
    conn = pymysql.connect(user='root', password='asdf1234', db='fs0tool', host='127.0.0.1', port=13306)
    c = conn.cursor()
    return conn, c




# Route for the home page (requires login)
@views.route('/', methods=['GET', 'POST'])
@login_required

def home():
    record = []
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
            
            # Assuming you have a function sql_connector() that returns the connection and cursor
            conn, c = sql_connector()


            # Your existing code
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

            # Add the new columns
 

            c.execute("""
                INSERT INTO reviews (
                    review_type, title, owner, category, sol_area, req_area,
                    release_label, rat, review_start_date, review_end_date,
                    primary_tm, sign_off, review_summary,
                    technical_manager, ra_lead_4g, ra_lead_5g, fs1ta_owner, system_architect,
                    other_mandatory, optional_reviewers, fst, apo, other_optional,
                    comp1, comp2, comp3, comp4, comp5, comp6, comp7
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)
            """, (
                review_type, title, owner, category, sol_area, req_area,
                release_label, rat, review_start_date, review_end_date,
                primary_tm, sign_off, review_summary,
                technical_manager, ra_lead_4g, ra_lead_5g, fs1ta_owner, system_architect,
                other_mandatory, optional_reviewers, fst, apo, other_optional,
                comp1, comp2, comp3, comp4, comp5, comp6, comp7
            ))


            # Commit the transaction and close the connection
            conn.commit()
            conn.close()

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
            
            record= list(c.fetchone())

            print(record)
            print(type(record))
            if record:
                # Unpack the record, assuming it has the expected number of values
                num, review_type, title, owner,  _, _, _, release_label, rat, review_start_date, review_end_date, primary_tm, sign_off, review_summary ,technical_manager, ra_lead_4g, ra_lead_5g, fs1ta_owner, system_architect, other_mandatory, optional_reviewers, fst, apo, other_optional, comp1, comp2, comp3, comp4, comp5, comp6, comp7 = record

                flash('Record found!', category='success')
            else:
                flash('No rec   ord found for the specified criteria.', category='error')
                


        elif 'StatusButton' in request.form:
            conn, c = sql_connector()
            stat= list(c.fetchall())
            c.execute("SELECT * FROM comments;")
            conn.commit()
            conn.close()
            

            print(stat)
            

    return render_template('home.html', user=current_user  , record1 = record)

# Route for the comment page (requires login)
@views.route('/comment', methods=['GET', 'POST'])
@login_required
def comment():
    record2 = []
    heading = ("Project ID", "Page/Slide", "Chapter/Section", "Review Comment", "Seriousness", "Reviewers email id", "Correction Status", "Correction Comments", "Agreed with reviewer (to be updated by the reviewer)")
    local_project_id = request.form.get('local_project_id')
    id1 = request.form.get('id1')
    # Connect to the database
    conn, c = sql_connector()

    # Retrieve all records from the comments table
    c.execute("SELECT * FROM comments;")
    record2 = list(c.fetchall())

    # Close the database connection
    conn.close()

    # Process the input if the request method is POST
    if request.method == 'POST':
        if 'savecomm' in request.form:
            # Connect to the database again for inserting a new record
            conn, c = sql_connector()

            # Get form data
            id1 = request.form.get('id1')
            Pages1 = request.form.get('page1')
            chapt1 = request.form.get('chapt1')
            rc1 = request.form.get('rc1')
            seri = request.form.get('seri')
            rev_email = current_user.email
            corr_stat = request.form.get('corr_stat')
            corr_comm = request.form.get('corr_comm')
            agree = request.form.get('agree')
            local_project_id = request.form.get('local_project_id')
            print("\n Local Project ID:", local_project_id)
            # Insert query
            c.execute("""
                INSERT INTO comments (
                    id, page, chapter, review_comment, seriousness, reviewer_email,
                    correction_status, correction_comments, agreed_with_reviewer
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                id1, Pages1, chapt1, rc1, seri, rev_email, corr_stat, corr_comm, agree
            ))

            # Commit the transaction and close the connection
            conn.commit()
            conn.close()

            flash('Review added!', category='success')

    # Render the template with the retrieved records and other data
    return render_template('comment.html', user=current_user, record2=record2, heading=heading)


@login_required
@views.route('/process_input', methods=['POST'])
def process_input():
    local_project_id = request.form.get('local_project_id')
    print("Local Project ID:", local_project_id)
    # Process the input or use it as needed

    return render_template('comments.html', local_project_id=local_project_id)

# @views.route('/comment', methods=['GET', 'POST'])
# @login_required
# def commentref():
        
#     heading = ("Project ID", "Page/Slide", "Chapter/Section", "Review Comment", "Seriousness", "Reviewers email id", "Correction Status", "Correction Comments", "Agreed with reviewer (to be updated by the reviewer)")

#     return render_template('comment.html', user=current_user  , heading= heading )



# Route for logging out (requires login)    
@views.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect(url_for('views.login'))




