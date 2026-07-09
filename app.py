import logging
import re
import smtplib
import os
from flask import Flask, render_template, request

from mail_config import SENDER_EMAIL, APP_PASSWORD, RESUME_FILE
from mail_body import SUBJECT, BODY
from send_email import send_single_email

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

EMAIL_REGEX = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/send', methods=['POST'])
def send():
    recipient = request.form.get('email', '').strip()

    # Validate email
    if not recipient or not EMAIL_REGEX.match(recipient):
        logger.warning("Invalid email submitted: %s", recipient)
        return render_template('index.html', error="Please enter a valid email address.")

    # Resolve resume path relative to this file
    resume_path = os.path.join(os.path.dirname(__file__), RESUME_FILE)

    try:
        send_single_email(
            sender_email=SENDER_EMAIL,
            app_password=APP_PASSWORD,
            recipient_email=recipient,
            subject=SUBJECT,
            body=BODY,
            resume_file=resume_path
        )
        logger.info("Email successfully sent to %s", recipient)
        return render_template('index.html', success=f"Email sent successfully to {recipient}!")

    except FileNotFoundError as e:
        logger.error("Resume file missing: %s", e)
        return render_template('index.html', error="Resume file not found. Please contact the administrator.")

    except smtplib.SMTPAuthenticationError:
        logger.error("SMTP authentication failed for sender %s", SENDER_EMAIL)
        return render_template('index.html', error="Email authentication failed. Please check SMTP credentials.")

    except (smtplib.SMTPException, OSError) as e:
        logger.error("Failed to send email to %s: %s", recipient, e)
        return render_template('index.html', error="Failed to send email due to a network or server error. Please try again.")


if __name__ == '__main__':
    app.run(debug=False)
