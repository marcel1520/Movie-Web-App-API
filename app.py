from flask import Flask, request, render_template, url_for, redirect, flash
from data_manager import SQLiteDataManager
from fetch_movie_data import fetch_movie_info
from dotenv import load_dotenv
import os

load_dotenv(".env")

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


data_manager = SQLiteDataManager(app)


@app.route('/')
@app.route('/users', methods=['GET', 'POST'])
def users():
    """
        Handles displaying all users and adding a new user.
        GET:
            - Retrieves all users from the database and renders them in the 'users.html' template.
        POST:
            - Adds a new user with the provided name from the form.
            - Redirects back to the users page after adding.
        Returns:
            Rendered HTML template or redirect response.
        """
    if request.method == 'GET':
        db_users = data_manager.get_all_users()
        return render_template('users.html', users=db_users)

    elif request.method == 'POST':
        name = request.form['name']
        data_manager.add_user({'name': name})
        return redirect(url_for('users'))


@app.route('/users/<int:user_id>/movies', methods=['GET', 'POST'])
def user_movies(user_id):
    """
        Displays and manages a user's movie collection.
        GET:
            - Fetches and displays all movies for the specified user.
        POST:
            - Fetches movie data by title using an external API.
            - Adds the movie to the user's collection if found.
            - Displays appropriate flash messages for errors or warnings.
        Args:
            user_id (int): The ID of the user whose movies are being managed.
        Returns:
            Rendered HTML template or redirect response.
        """
    if request.method == 'POST':
        title = request.form.get('title')
        if not title:
            flash("Provide title", "Warning")
            return redirect(url_for('user_movies', user_id=user_id))
        try:
            movie_data = fetch_movie_info(title)
            if movie_data:
                data_manager.add_movie(user_id, movie_data)
            else:
                flash("Movie not found", "Error")
        except KeyError as k:
            flash("No Movie found, check spelling", "Error")

        return redirect(url_for('user_movies', user_id=user_id))

    user = data_manager.get_user(user_id)
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user=user, movies=movies)


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """
        Deletes a movie from a user's collection.
        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie to delete.
        Returns:
            Redirects to the user's movie page.
        """
    data_manager.delete_movie(user_id, movie_id)
    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """
        Deletes a user and all associated data.
        Args:
            user_id (int): The ID of the user to delete.
        Returns:
            Redirects to the users listing page.
        """
    data_manager.delete_user(user_id)
    return redirect(url_for('users'))


if __name__ == "__main__":
    app.run(debug=True)

