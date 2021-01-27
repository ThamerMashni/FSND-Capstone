import os
from flask import Flask, request, abort, jsonify, url_for, render_template, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
import sys
from auth import AuthError, requires_auth
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
import json
from functools import wraps




def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__,
                static_url_path='',
                static_folder='templates/public',
                template_folder='templates')

    oauth = OAuth(app)
    app.secret_key = "jwtsecrtkey"

    auth0 = oauth.register(
        'auth0',
        client_id='vcylBDMoFwrLB19THy7t7MlMEY4JJkXS',
        client_secret='KBH9eTEyZzSD7OP3L5EfnxrOHwHEjWkS2MqlGfqrLiWD1yxPXbyNI7at-ZK1tFF5',
        api_base_url='https://mashni.eu.auth0.com',
        access_token_url='https://mashni.eu.auth0.com/oauth/token',
        authorize_url='https://mashni.eu.auth0.com/authorize',
        client_kwargs={
            'scope': 'openid profile email',
        },
    )

    def requires_login(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'profile' not in session:
                # Redirect to Login page here
                return redirect('/')
            return f(*args, **kwargs)
    
        return decorated
        
    @app.route('/callback')
    def callback_handling():
        # Handles response from token endpoint
        auth0.authorize_access_token()
        resp = auth0.get('userinfo')
        userinfo = resp.json()

        # Store the user information in flask session.
        session['jwt_payload'] = userinfo
        session['profile'] = {
            'user_id': userinfo['sub'],
            'name': userinfo['name'],
            'picture': userinfo['picture']
        }
        return redirect('/dashboard')

    @app.route('/login')
    def login():
        return auth0.authorize_redirect(redirect_uri='http://localhost:8080/callback')

        
    @app.route('/logout')
    def logout():
        # Clear session stored data
        session.clear()
        # Redirect user to logout endpoint
        params = {'returnTo': url_for('index', _external=True), 'client_id': 'vcylBDMoFwrLB19THy7t7MlMEY4JJkXS'}
        return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))
   
    @app.route('/dashboard')
    @requires_login
    def dashboard():
        return render_template('dashboard.html',
                               userinfo=session['profile'],
                               userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE')
        return response

    @app.route('/')
    def index():
        return render_template('index.html')

    # GETs

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def retrive_actors(jwt):
        try:
            actors = Actor.query.order_by(Actor.id).all()
            formated_actors = []
            for actor in actors:
                formated_actors.append(actor.format())

            return jsonify({
                'success': True,
                'actors': formated_actors,
            })
        except Exception:
            abort(404)

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def retrive_movies(jwt):
        try:
            movies = Movie.query.order_by(Movie.id).all()
            formated_movies = []
            for movie in movies:
                formated_movies.append(movie.format())

            return jsonify({
                'success': True,
                'movies': formated_movies,
            })
        except Exception:
            abort(404)

    # POSTs

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(jwt):
        body = request.get_json()
        try:

            actor = Actor(body['name'], body['age'], body['gender'])
            actor.insert()

            return jsonify({
                'success': True,
                'actor': actor.format()
            })
        except Exception:
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(jwt):
        body = request.get_json()
        try:
            movie = Movie(body['title'], body['release_date'])
            movie.actors = body['actors']
            movie.insert()

            return jsonify({
                'success': True,
                'movies': movie.id,
            })
        except Exception:
            abort(422)

    # DELETEs

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            actor.delete()

            return jsonify({
                "success": True,
                "deleted": actor_id
            })
        except Exception:
            abort(404)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            movie.delete()

            return jsonify({
                "success": True,
                "deleted": movie_id
            })
        except Exception:
            abort(404)

    # PATCHes

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(jwt, id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if movie is None:
            abort(404)

        body = request.get_json()
        try:
            keys = body.keys()
            if 'title' in keys:
                movie.title = body['title']
            if 'release_date' in keys:
                movie.recipe = body['release_date']
            if 'actors' in keys:
                movie.actors = body['actors']
            movie.update()
        except Exception:
            abort(422)

        return jsonify({
            "success": True,
            "movie": movie.format()
        })

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(jwt, id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if actor is None:
            abort(404)

        body = request.get_json()
        keys = body.keys()
        try:
            if 'name' in keys:
                actor.name = body['name']
            if 'age' in keys:
                actor.age = body['age']
            if 'gender' in keys:
                actor.actors = body['gender']
            actor.update()
        except Exception:
            abort(422)

        return jsonify({
            "success": True,
            "actor": actor.format()
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 405

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='localhost', port=8080, debug=True)
