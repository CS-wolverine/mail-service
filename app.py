import logging
import re
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from flask import Flask, render_template, request

# ── Logging ────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# ── Config ─────────────────────────────────────────────────────────
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "shahc5636@gmail.com")
APP_PASSWORD  = os.environ.get("APP_PASSWORD", "")
SMTP_HOST     = "smtp.gmail.com"
SMTP_PORT     = 587
RESUME_FILE   = "Chandan_software_developer.pdf"

# ── Email content ──────────────────────────────────────────────────
SUBJECT = "Looking for Software Engineer Opportunities | 2+ YOE | MCA (NIT Bhopal)"

BODY = """Hi,

I hope you're doing well.

I am reaching out to express my interest in Software Engineer / Software Development opportunities within your organization. If there are any suitable openings, I would be grateful if you could consider my profile.

I have 2+ years of experience in software development, primarily working with Python, Django, FastAPI, REST APIs, MySQL, MongoDB, AWS, Docker, Kafka, and PySpark. I have experience building scalable backend applications, developing production-ready APIs, working on AI-powered Computer Vision solutions, and building real-time data processing systems.

I am currently working in Pune, open to relocation, and have a 30-day notice period.

Please find my resume attached for your review. I would sincerely appreciate your consideration for any current or upcoming opportunities that align with my experience.

Thank you for your time and consideration. I look forward to hearing from you.

Best regards,

Chandan Shah
Software Engineer
📞 +91 7869134677
✉️ shahc5636@gmail.com
🔗 LinkedIn: https://linkedin.com/in/chandan-shah-571a88222
💻 GitHub: https://github.com/cswolverine
"""

# ── Flask app ──────────────────────────────────────────────────────
app = Flask(__name__)
EMAIL_REGEX = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')


def send_email(recipient_email):
    resume_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), RESUME_FILE)

    logger.info("=== START send_email to: %s ===", recipient_email)
    logger.info("SENDER_EMAIL: %s", SENDER_EMAIL)
    logger.info("APP_PASSWORD set: %s", bool(APP_PASSWORD))
    logger.info("Resume path: %s", resume_path)
    logger.info("Resume exists: %s", os.path.exists(resume_path))

    if not os.path.exists(resume_path):
        raise FileNotFoundError(f"Resume not found at: {resume_path}")

    if not APP_PASSWORD:
        raise ValueError("APP_PASSWORD env variable is not set")

    # Build message
    logger.info("Building email message...")
    msg = MIMEMultipart()
    msg['From']    = SENDER_EMAIL
    msg['To']      = recipient_email
    msg['Subject'] = SUBJECT
    msg.attach(MIMEText(BODY, 'plain'))

    with open(resume_path, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={RESUME_FILE}')
        msg.attach(part)
    logger.info("Email message built successfully")

    # Send
    logger.info("Connecting to SMTP %s:%s ...", SMTP_HOST, SMTP_PORT)
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=60) as server:
        logger.info("Connected. Starting TLS...")
        server.starttls()
        logger.info("TLS started. Logging in...")
        server.login(SENDER_EMAIL, APP_PASSWORD)
        logger.info("Login successful. Sending message...")
        server.send_message(msg)

    logger.info("=== Email sent successfully to: %s ===", recipient_email)


@app.route('/', methods=['GET'])
def index():
    logger.info("GET / — serving index page")
    return render_template('index.html')


@app.route('/send', methods=['POST'])
def send():
    recipient = request.form.get('email', '').strip()
    logger.info("POST /send — recipient: %s", recipient)

    if not recipient or not EMAIL_REGEX.match(recipient):
        logger.warning("Invalid email: %s", recipient)
        return render_template('index.html', error="Please enter a valid email address.")

    try:
        send_email(recipient)
        return render_template('index.html', success=f"Email sent successfully to {recipient}!")

    except FileNotFoundError as e:
        logger.error("FileNotFoundError: %s", e)
        return render_template('index.html', error="Resume file not found on server.")

    except ValueError as e:
        logger.error("ValueError: %s", e)
        return render_template('index.html', error="Server misconfiguration. APP_PASSWORD not set.")

    except smtplib.SMTPAuthenticationError as e:
        logger.error("SMTPAuthenticationError: %s", e)
        return render_template('index.html', error="Gmail authentication failed. Check APP_PASSWORD.")

    except smtplib.SMTPException as e:
        logger.error("SMTPException: %s", e)
        return render_template('index.html', error=f"SMTP error: {e}")

    except Exception as e:
        logger.error("Unexpected error: %s", e, exc_info=True)
        return render_template('index.html', error=f"Unexpected error: {e}")


if __name__ == '__main__':
    app.run(debug=False)
