import os

# SMTP configuration — values set as environment variables on Render
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "shahc5636@gmail.com")
APP_PASSWORD = os.environ.get("APP_PASSWORD", "")
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
RESUME_FILE = "Chandan_software_developer.pdf"
