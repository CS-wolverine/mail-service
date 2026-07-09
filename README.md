# Resume Mailer — Flask Web App

A simple Flask web app to send your resume to a recruiter's email address with one click.

---

## Project Structure

```
project/
├── app.py                          # Flask application
├── send_email.py                   # Email sending logic
├── mail_config.py                  # SMTP credentials & config
├── mail_body.py                    # Email subject & body
├── Chandan_software_developer.pdf  # Resume attachment
├── requirements.txt
├── Procfile
├── .gitignore
├── README.md
├── templates/
│   └── index.html
└── static/
    └── style.css
```

---

## Run Locally

```bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the Flask dev server
python app.py
```

Open http://127.0.0.1:5000 in your browser.

---

## Run with Gunicorn (production-style)

```bash
gunicorn app:app
```

Open http://127.0.0.1:8000 in your browser.

---

## Deploy on Render

1. Push this project to a GitHub repository.
2. Go to https://render.com and create a **New Web Service**.
3. Connect your GitHub repo.
4. Set the following:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Click **Deploy**. Render will detect the `Procfile` automatically.

> Make sure `Chandan_software_developer.pdf` is committed to the repo so it's available at runtime.

---

## Endpoints

| Method | Path    | Description                        |
|--------|---------|------------------------------------|
| GET    | `/`     | Renders the email input form       |
| POST   | `/send` | Validates email and sends resume   |
# mail-service
# mail-service
