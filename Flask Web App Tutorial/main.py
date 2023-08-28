from aiohttp import request
from flask import redirect, render_template, url_for
from website import create_app
# app.py
import random
from flask import Flask, render_template, request, redirect, url_for, session

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        # Process the form data, generate OTP, and send email/SMS
        # Redirect to the OTP verification page
        return redirect(url_for('verify_otp'))
    return render_template('forgot_password.html')



# app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ... your existing routes ...

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        user_otp = request.form.get('otp')
        saved_otp = session.get('otp')

        if user_otp == saved_otp:
            return redirect(url_for('reset_password.html'))
        else:
            error_message = 'Invalid OTP. Please try again.'
            return render_template('verify_otp.html', error_message=error_message)

    return render_template('verify_otp.html')

# ... other routes ...
@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        # Update the user's password in the database
        return redirect(url_for('login'))  # Redirect to login page

    return render_template('reset_password.html')

from flask import Flask, render_template, request, redirect, url_for
import pyotp
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Simulated database (replace with a proper database setup)
users_db = {}

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        if email in users_db:
            otp_secret = pyotp.random_base32()
            otp = pyotp.TOTP(otp_secret)
            users_db[email]['otp_secret'] = otp_secret

            # Send the OTP to the user's email
            send_otp_email(email, otp.now())

            return redirect(url_for('verify_otp'))
    return render_template('forgot_password.html')

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        email = request.form['email']
        entered_otp = request.form['otp']
        if email in users_db and 'otp_secret' in users_db[email]:
            otp = pyotp.TOTP(users_db[email]['otp_secret'])
            if otp.verify(entered_otp):
                return redirect(url_for('reset_password'))
    return render_template('verify_otp.html')

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new_password']
        if email in users_db:
            # Update the password in the database (ensure secure password storage)
            users_db[email]['password'] = hash_and_salt_password(new_password)
            return "Password reset successful."
    return render_template('reset_password.html')

def send_otp_email(email, otp):
    # Configure and send the OTP email here
    # Use Flask-Mail or another email service
    pass

def hash_and_salt_password(password):
    # Implement secure password hashing and salting
    pass

if __name__ == '__main__':
    app.run()
