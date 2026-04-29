import smtplib
from flask import Flask, render_template, request
import requests
import os

# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()
OWN_EMAIL = os.environ.get("OWN_EMAIL")
OWN_PASSWORD = os.environ.get("OWN_PASSWORD")

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html", msg_sent=False)
    else:
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")
        try:
            send_email(name, email, phone, message)
            print("Email sent successfully!")
            return render_template("contact.html", msg_sent=True)
        except smtplib.SMTPAuthenticationError:
            print("Error: Authentication failed. Check your email/password.")
            return render_template("contact.html", msg_sent=False)
        except smtplib.SMTPException as e:
            print(f"Error: SMTP error occurred: {e}")
            return render_template("contact.html", msg_sent=False)
        except Exception as e:
            print(f"Error: An unexpected error occurred: {e}")
            return render_template("contact.html", msg_sent=False)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

def send_email(name, email, phone, message):
    email_message = f"Subject:New Message from python contact\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=OWN_EMAIL, password=OWN_PASSWORD)
        connection.sendmail(
            from_addr=OWN_EMAIL,
            to_addrs=OWN_EMAIL,
            msg=email_message
        )

if __name__ == "__main__":
    app.run(debug=True, port=5001)
