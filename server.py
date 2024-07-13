import os
from flask import Flask, request, render_template
import smtplib

app = Flask(__name__)

MY_EMAIL = os.getenv("MY_EMAIL", "lulu.triana09@gmail.com")
MY_PASSWORD = os.getenv("MY_PASSWORD", "mhqy rthn qtjv ggws")


@app.route("/")
def home():
    return render_template("index.html", msg_sent=False)


@app.route("/contact", methods=["POST"])
def contact():
    if request.method == "POST":
        data = request.form
        try:
            send_email(data["name"], data["email"], data["subject"], data["message"])
            return render_template("index.html", msg_sent=True)
        except smtplib.SMTPResponseException as e:
            error_code = e.smtp_code
            error_message = e.smtp_error.decode() if e.smtp_error else 'No error message'
            print(f"SMTP error code: {error_code}")
            print(f"SMTP error message: {error_message}")
            return render_template("index.html", msg_sent=False, error=error_message)
        except Exception as e:
            print(f"An error occurred: {e}")
            return render_template("index.html", msg_sent=False, error=str(e))


def send_email(name, email, subject, message):
    email_message = f"Subject: New Message\n\nName: {name}\nEmail: {email}\nSubject: {subject}\nMessage: {message}"
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.set_debuglevel(1)
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(MY_EMAIL, MY_EMAIL, email_message)


if __name__ == "__main__":
    app.run(debug=False)
