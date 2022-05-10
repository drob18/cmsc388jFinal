from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import movie_client
from ..forms import MovieReviewForm, SearchForm, SearchUserForm
from ..models import User, Review
from ..utils import current_time


movies = Blueprint('movies',__name__)
main = Blueprint('main', __name__)

@movies.route("/users", methods=["GET", "POST"])
def search_users():
    form = SearchUserForm()
    print("HERE0")
    if form.validate_on_submit():
        print("HERE1")
        return redirect(url_for("movies.query_users", query=form.query.data))
    print()
    return render_template("searchUser.html", form=form)

@movies.route("/users/search-results/<query>", methods=["GET"])
def query_users(query):
    try:
        print("HERE2")
        results = User.objects(username=query).first()
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("movies.search_users"))

    return render_template("userQuery.html", results=results)

@movies.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    reviews = Review.objects(commenter=user)

    return render_template("user_detail.html", username=username, reviews=reviews)

@movies.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("movies.query_results", query=form.search_query.data))

    return render_template("index.html", form=form)


@movies.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    try:
        results = movie_client.search(query)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("movies.index"))

    return render_template("query.html", results=results)


@movies.route("/movies/<movie_id>", methods=["GET", "POST"])
def movie_detail(movie_id):
    try:
        result = movie_client.retrieve_movie_by_id(movie_id)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("movies.index"))

    form = MovieReviewForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            imdb_id=movie_id,
            movie_title=result.title,
            reviewerType=current_user._get_current_object().accountType,
            score = form.score.data

        )

        review.save()

        return redirect(request.path)

    
    """
        Check if the person is critic or normal then change that list by adding the new score
        result.normalScore.apped(form.score.data)
        """

    reviews = Review.objects(imdb_id=movie_id)

    scoreList = []
    for curr in reviews:
        scoreList.append(curr.score)
    

        if (current_user._get_current_object().accountType == "Terp Critic"):
            
            result.updateTerpScore(curr.score)
                
        elif (current_user._get_current_object().accountType == "Normal Critic"):
            result.updateNormalpScore(curr.score)

    
    print("this is the list: " + str(result.terpScores))
    return render_template(
        "movie_detail.html", form=form, movie=result, reviews=reviews)