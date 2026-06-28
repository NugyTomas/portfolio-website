from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, Text

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


# with app.app_context():
#     db.create_all()

# new_project = Project(name="Jo Code Translator",
#                       description="A Python command-line application that translates text to Morse code and vice versa.",
#                       image="projects/morse.png", github_link="https://github.com/NugyTomas/morse-code-translator",
#                       featured_on_main_page=True, )
# with app.app_context():
#     db.session.add(new_project)
#     db.session.commit()


@app.route('/')
def home():
    projects = db.session.execute(db.select(Project)).scalars().all()
    return render_template("index.html", projects=projects)


if __name__ == "__main__":
    app.run(debug=True)
