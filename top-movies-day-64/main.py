from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DB

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///top-movies.db"

# Create the extension
db = SQLAlchemy(model_class=Base)
# Initialise the app with the extension
db.init_app(app)

# CREATE TABLE

class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    # Optional: this will allow each movie object to be identified by its title when printed.
    def __repr__(self):
        return f'<Movie {self.title}, {self.rating}>'

# Create table schema in the database. Requires application context.
with app.app_context():
    db.create_all()

    movie = db.session.execute(
        db.select(Movie).where(Movie.title == "Phone Booth")
    ).scalar()

    if not movie:
        new_movie = Movie(title="Phone Booth", year=2002,
                          description="Publicist Stuart Shepard finds himself trapped in a phone booth, "
                                      "pinned down by an extortionist's sniper rifle. Unable to leave or "
                                      "receive outside help, Stuart's negotiation with the caller leads "
                                      "to a jaw-dropping climax.",
                     rating=7.3, ranking=10, review="My favourite character was the caller.",
                          img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg")
        db.session.add(new_movie)
        second_movie = Movie(title="Avatar The Way of Water",
                            year=2022,
                            description="Set more than a decade after the events of the first film, "
                                        "learn the story of the Sully family (Jake, Neytiri, "
                                        "and their kids), the trouble that follows them, the lengths "
                                        "they go to keep each other safe, the battles they fight to "
                                        "stay alive, and the tragedies they endure.",
                            rating=7.3,
                            ranking=9,
                            review="I liked the water.",
                            img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
                            )
        db.session.add(second_movie)
        db.session.commit()

class RatingForm(FlaskForm):
    rating = StringField('Your Rating Out of 10, e.g. 7.5', validators=[DataRequired()])
    review = StringField('Your Review', validators=[DataRequired()])
    submit = SubmitField('Done')

class AddForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')


@app.route("/")
def home():
    with app.app_context():
        result = db.session.execute(db.select(Movie).order_by(Movie.rating))
        all_movies = result.scalars().all()
        length = len(all_movies)
        for movie in all_movies:
            movie.ranking = length
            length -= 1

    return render_template('index.html', movies=all_movies)


@app.route("/edit",  methods=["GET", "POST"])
def edit():
    form = RatingForm()
    movie_id = request.args.get('id')
    movie_selected = db.get_or_404(Movie, movie_id)

    if form.validate_on_submit():
        movie_selected.rating = float(form.rating.data)
        movie_selected.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit.html', movie=movie_selected, form=form)

@app.route("/delete")
def delete():
    movie_id = request.args.get('id')
    movie = db.get_or_404(Movie, movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/add", methods=["GET", "POST"])
def add_movie():
    form = AddForm()
    access_token = os.environ.get('ACCESS_TOKEN')

    if form.validate_on_submit():
        title = form.title.data
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        try:
            response = requests.get(url=f"https://api.themoviedb.org/3/search/movie?query={title}", headers=headers )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("The movie db is not available")
            if e.response:
                print(e.response.text)

        else:
            data = response.json()
            movies = data["results"]
            movies_selected = []
            for movie in movies:
                movies_selected.append({
                "id": movie["id"],
                "title": movie["title"],
                "date": movie["release_date"],
                })

            return render_template("select.html", movies=movies_selected)


    return render_template('add.html', form=form)

@app.route("/insert-movie")
def insert_movie():
    movie_id = request.args.get('id')
    access_token = os.environ.get('ACCESS_TOKEN')

    headers = {
            "Authorization": f"Bearer {access_token}"
        }

    try:
        response = requests.get(url=f"https://api.themoviedb.org/3/movie/{movie_id}", headers=headers )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("The movie db is not available")
        if e.response:
            print(e.response.text)
    else:
        data = response.json()
        date = data["release_date"]
        year = datetime.strptime(date, "%Y-%m-%d").year
        image_path = data["poster_path"]
        image_url = f"https://image.tmdb.org/t/p/w500{image_path}"
        with app.app_context():
            new_movie_from_selection = Movie(title=data["title"],
                                             year=year,
                                            description=data["overview"],
                                            img_url=image_url
                                        )
            db.session.add(new_movie_from_selection)
            db.session.commit()
            new_id = new_movie_from_selection.id
        return redirect(url_for('edit', id=new_id))

if __name__ == '__main__':
    app.run(debug=True)
