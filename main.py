from datetime import datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, Text
import os
import dotenv
import smtplib
from email.message import EmailMessage

dotenv.load_dotenv()

MY_EMAIL = os.environ.get("MY_EMAIL")
PASSWORD = os.environ.get("PASSWORD")

app = Flask(__name__)


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///portfolio.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


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


# new_project = Project(name="Jo Code Translator",
#                       description="A Python command-line application that translates text to Morse code and vice versa.",
#                       image="projects/morse.png", github_link="https://github.com/NugyTomas/morse-code-translator",
#                       featured_on_main_page=True, )
# with app.app_context():
#     db.session.add(new_project)
#     db.session.commit()

# new_skill = Skill(name="Selenium",
#                   image="skills/selenium.png")
#
# with app.app_context():
#     db.session.add(new_skill)
#     db.session.commit()

@app.context_processor
def inject_year():
    return {
        "current_year": datetime.now().year
    }


@app.route('/')
def home():
    projects = db.session.execute(db.select(Project)).scalars().all()
    skills = db.session.execute(db.select(Skill)).scalars().all()
    return render_template("index.html", navbar="contact", projects=projects, skills=skills)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        data = request.form
        send_email(data)
        return render_template("contact.html", navbar="home")
    return render_template("contact.html", navbar="home")


def send_email(data):
    email = EmailMessage()
    email["Subject"] = "New message from TNG website"
    email["From"] = MY_EMAIL
    email["To"] = MY_EMAIL

    email.set_content(
        f"""
Name: {data['name']}
Email: {data['email']}

Message:
{data['message']}
"""
    )
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(MY_EMAIL, PASSWORD)
        connection.send_message(email)


if __name__ == "__main__":
    app.run(debug=True)
