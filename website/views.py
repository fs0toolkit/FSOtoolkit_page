from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from .models import User, Review, Comment
from . import db
from flask import Flask, render_template, request
import pymysql
from datetime import datetime 
import re
import requests
import adal


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

# Route for the signup page


# Route for the home page (requires login)
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('views.login'))


    if request.method == 'POST':
        if 'Resetbutton' in request.form:
            # if request.form.get('Resetbutton'):
        # Capture form data
            review_type = request.form.get('review_type')
            title = request.form.get('Titleinput')
            owner = current_user.email  # Use the email of the logged-in user
            category = request.form.get('review_type2')
            sol_area = request.form.get('dropdown3')
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





    elif request.method == 'GET':
        # if request.form.get('updatebutton'):
        # if 'updatebutton' in request.form:
        # Capture form data
            # Capture form data for retrieving an existing record
        print("inside get req")
        category = request.form.get('review_type2')
        sol_area = request.form.get('dropdown3')
        req_area = request.form.get('review_type4')
        print(sol_area , req_area ,category )
        conn, c = sql_connector()
        # Retrieve a record from the 'reviews' table based on the combination of criteria
        c.execute("""
            SELECT *
            FROM reviews
            WHERE sol_area = %s AND req_area = %s AND category = %s
        """, (category , sol_area, req_area))
        # record =  0
        record = c.fetchone()
        print("helolo1 \n")
        print(record)
        if record:
            # Populate the form inputs with the retrieved record's values
            review_type, title, owner, _, _, _, release_label, rat, review_start_date, review_end_date, primary_tm, sign_off, review_summary = record
            flash('Record found!', category='success')
                        
            # Split the input string into key-value pairs based on "&"
        #     key_value_pairs = record.split('&')

        #     # Create a dictionary to store the filtered keys
        #     filtered_data = {}
        #     print("helolo \n")
        #     # Define a regular expression pattern to match keys starting with "review_type" followed by a number
        #     pattern = re.compile(r'review_type(\d+)')

        #     # Iterate through the key-value pairs
        #     for pair in key_value_pairs:
        #         # Split each pair into key and value based on "="
        #         key, value = pair.split('=')
                
        #         # Check if the key matches the pattern
        #         match = pattern.match(key)
        #         if match:
        #             # Extract the number from the key
        #             number = match.group(1)
                    
        #             # Map the extracted keys to the desired names
        #             mapping = {
        #                 "1": "review_type",
        #                 "2": "title",
        #                 "3": "owner",
        #                 "4": "rat",
        #                 "5": "review_start_date",
        #                 "6": "review_end_date",
        #                 "7": "primary_tm",
        #                 "8": "sign_off",
        #                 "9": "review_summary"
        #             }
                    
        #             # Use the mapping to get the desired key name
        #             desired_key = mapping.get(number, f"review_type{number}")
                    
        #             # Store the desired key and value in the dictionary
        #             filtered_data[desired_key] = value

        #     # Print the resulting dictionary
        #             # print(filtered_data)
        #             print("helolo \n")






        #     # print(record)
        # else:
        #     flash('No record found for the specified criteria.', category='error')
            
    # record = '23R1'
    # print(record)
    return render_template('home.html', user=current_user )








# request.method = 'GET'
# a = home()
# print(a)










                    # elif request.form.get('reset_button'):
    
        #     if row:
        #         # Populate the form fields with values from the 'default' table
        #         review_type = row['Cloud_Assignment']
        #         title = row['Operability_Assignment']
        #         # Continue populating other fields as well

        # elif request.form.get('UpdateButton'):






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




