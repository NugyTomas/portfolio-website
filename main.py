# =========================================
# IMPORTS
# =========================================
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, Text
import os
import dotenv
import smtplib
from email.message import EmailMessage

# =========================================
# CONFIGURATION
# =========================================
dotenv.load_dotenv()

MY_EMAIL = os.environ.get("MY_EMAIL")
PASSWORD = os.environ.get("PASSWORD")

app = Flask(__name__)


class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///portfolio.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# =========================================
# DATABASE MODELS
# =========================================
class Project(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    image: Mapped[str] = mapped_column(String(250), nullable=False)
    github_link: Mapped[str] = mapped_column(String(250), nullable=False)
    featured_on_main_page: Mapped[bool] = mapped_column(Boolean, nullable=False)


class Skill(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    image: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()

# =========================================
# CONTEXT PROCESSOR - GETS CURRENT YEAR
# =========================================
@app.context_processor
def inject_year():
    return {
        "current_year": datetime.now().year
    }

# =========================================
# ROUTES
# =========================================
@app.route('/')
def home():
    projects = db.session.execute(db.select(Project)).scalars().all()
    skills = db.session.execute(db.select(Skill)).scalars().all()
    return render_template("index.html", projects=projects, skills=skills)

@app.route('/all_projects')
def all_projects():
    projects = db.session.execute(db.select(Project)).scalars().all()
    return render_template("projects.html", projects=projects)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form

        if send_email(data):
            return redirect(url_for("contact", sent=1))

        return render_template("contact.html", show_success=False, error=True
        )

    return render_template(
        "contact.html", show_success=request.args.get("sent"), error=False
    )

# =========================================
# HELPER FUNCTION
# =========================================
def send_email(data):
    try:
        email = EmailMessage()
        email["Subject"] = "New message from TNG website"
        email["From"] = MY_EMAIL
        email["To"] = MY_EMAIL

        email.set_content(
            f"Name: {data['name']}\n"
            f"Email: {data['email']}\n\n"
            f"Message:\n"
            f"{data['message']}"
        )

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, PASSWORD)
            connection.send_message(email)
        return True

    except Exception:
        return False

# =========================================
# APPLICATION ENTRY POINT
# =========================================
if __name__ == "__main__":
    app.run(debug=True)

