import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor
from Env import DB_TEST_NAME, DB_PASSWORD, DB_PORT, DB_USERNAME, DB_HOST
from Env import CASTING_ASSISTANT_TOKEN, CASTING_DIRECTOR_TOKEN, EXECUTIVE_PRODUCER_TOKEN
ACCESS_TOKEN = EXECUTIVE_PRODUCER_TOKEN

class appTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = 'postgres://'f'{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_TEST_NAME}'

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""

    # GET Endpints Tests
    def test_retrive_actors(self):
        headers = {
            'Authorization': 'Bearer {}'.format(ACCESS_TOKEN)
        }
        res = self.client().get('/actors', headers=headers)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 4)
    
    def test_fail_to_retrive_actors(self):
        headers = {
            'Authorization': 'Bearer {}'.format(ACCESS_TOKEN)
        }
        res = self.client().get('/actors/1000', headers=headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Method not allowed')

    def test_retrive_movies(self):
        headers = {
            'Authorization': 'Bearer {}'.format(ACCESS_TOKEN)
        }
        res = self.client().get('/movies', headers=headers)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 2)
    
    def test_fail_to_movies(self):
        headers = {
            'Authorization': 'Bearer {}'.format(ACCESS_TOKEN)
        }
        res = self.client().get('/movies/1000', headers=headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Method not allowed')
    
    # DELETE Endpoints Tests
    def test_delete_actor(self):
        headers = {
            'Authorization': 'Bearer {}'.format(ACCESS_TOKEN)
        }

        test_actor = Actor(name='actor1', age=50, gender='Male')
        test_actor.insert()

        res = self.client().delete(f'/actors/{test_actor.id}', headers=headers)
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == test_actor.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], test_actor.id)
        self.assertEqual(actor, None)

    def test_faild_to_delete_question(self):
        headers = {
            'Authorization': 'Bearer {}'.format(ACCESS_TOKEN)
        }
        res = self.client().delete('/actor/1000', headers=headers)
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')

    def test_delete_movie(self):
        headers = {
            'Authorization': 'Bearer {}'.format(ACCESS_TOKEN)
        }

        test_movie = Movie(title='movie1', release_date='02-02-2020')
        test_movie.insert()

        res = self.client().delete(f'/movies/{test_movie.id}', headers=headers)
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == test_movie.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], test_movie.id)
        self.assertEqual(movie, None)

    def test_faild_to_delete_movie(self):
        headers = {
            'Authorization': 'Bearer {}'.format(ACCESS_TOKEN)
        }
        res = self.client().delete('/movies/1000', headers=headers)
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')

    # POST Endponts Tests 
    
    def test_create_actor(self):
        headers = {
            'Authorization': 'Bearer {}'.format(ACCESS_TOKEN)
        }
        res = self.client().post('/actors',json={
            'name': "test_actor1",
            'age': 22,
            'gender':'Female'
        }, headers=headers)
        data=json.loads(res.data)
        
        actor = Actor.query.filter(Actor.name=='test_actor1').first()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['actor'],actor.format())
        actor.delete()
        

    def test_fail_to_create_actor(self):
        headers = {
            'Authorization': 'Bearer {}'.format(ACCESS_TOKEN)
        }
        res = self.client().post('/actors',json={
            'age': 22,
            'gender':'Female'
        }, headers=headers)
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"unprocessable")

    
    def test_create_movie(self):
        headers = {
            'Authorization': 'Bearer {}'.format(ACCESS_TOKEN)
        }
        res = self.client().post('/movies',json={
            'title': "test_movie1",
            'release_date': '02-02-2020',
            'actors': [] 
        }, headers=headers)
        data=json.loads(res.data)
        
        movie = Movie.query.filter(Movie.title=='test_movie1').first()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['movies'],movie.id)
        movie.delete()
        

    def test_fail_to_create_movie(self):
        headers = {
            'Authorization': 'Bearer {}'.format(ACCESS_TOKEN)
        }
        res = self.client().post('/movies',json={
            'title': "test_movie1"
        }, headers=headers)
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"unprocessable")

    # PATCH Endponts Tests 
    def test_update_actor(self):
        test_actor = Actor(name='test_actor1', age=20,gender='Male')
        test_actor.insert()

        headers = {
            'Authorization': 'Bearer {}'.format(ACCESS_TOKEN)
        }
        res = self.client().patch(f'/actors/{test_actor.id}',json={
            'name': "test_actor_patched",
            'age': 22,
            'gender':'Female'
        }, headers=headers)
        data=json.loads(res.data)
                
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['actor'],test_actor.format())
        test_actor.delete()

    def test_fail_to_update_actor(self):
        headers = {
            'Authorization': 'Bearer {}'.format(ACCESS_TOKEN)
        }
        res = self.client().patch(f'/actors/1000',json={
            'name': "test_actor_patched",
            'age': 22,
            'gender':'Female'
        }, headers=headers)
        data=json.loads(res.data)
                
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')

    def test_update_movie(self):
        test_movie = Movie(title='test_movie1', release_date='02-02-2020')
        test_movie.insert()

        headers = {
            'Authorization': 'Bearer {}'.format(ACCESS_TOKEN)
        }
        res = self.client().patch(f'/movies/{test_movie.id}',json={
            'title': "test_movie_patched",
            'release_date': '02-02-2020'
        }, headers=headers)
        data=json.loads(res.data)
                
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        test_movie.delete()

    def test_fail_to_update_movie(self):
        headers = {
            'Authorization': 'Bearer {}'.format(ACCESS_TOKEN)
        }
        res = self.client().patch(f'/movies/1000',json={
            'title': "test_movie_patched",
            'release_date': '02-02-2020'
        }, headers=headers)
        data=json.loads(res.data)
                
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
