import smtplib
import logging
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import csv

logger = logging.getLogger(__name__)


def _build_message(sender_email, recipient_email, subject, body, resume_file):
    """Build a MIMEMultipart email message with resume attachment."""
    if not os.path.exists(resume_file):
        raise FileNotFoundError(f"Resume not found: {resume_file}")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with open(resume_file, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename={os.path.basename(resume_file)}'
        )
        msg.attach(part)

    return msg


def send_single_email(sender_email, app_password, recipient_email, subject, body, resume_file):
    """Send one email with resume to a single recipient. Used by the Flask app."""
    msg = _build_message(sender_email, recipient_email, subject, body, resume_file)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)

    logger.info("Email sent to %s", recipient_email)


def send_emails(sender_email, app_password, recipients_csv, subject, body, resume_file):
    """Send cold emails with resume to all recipients from CSV."""
    with open(recipients_csv, 'r') as f:
        reader = csv.DictReader(f)
        recipients = [row['email'] for row in reader]

    total = len(recipients)
    sent = 0

    for recipient_email in recipients:
        try:
            send_single_email(sender_email, app_password, recipient_email, subject, body, resume_file)
            sent += 1
            print(f"[{sent}/{total}] Sent to {recipient_email}")
        except Exception as e:
            print(f"[{sent}/{total}] Failed to send to {recipient_email}: {e}")

    print(f"\nCompleted: {sent}/{total} emails sent successfully")


if __name__ == "__main__":
    from mail_config import SENDER_EMAIL, APP_PASSWORD, RESUME_FILE
    from mail_body import SUBJECT, BODY

    send_emails(
        sender_email=SENDER_EMAIL,
        app_password=APP_PASSWORD,
        recipients_csv="recipients.csv",
        subject=SUBJECT,
        body=BODY,
        resume_file=RESUME_FILE
    )
