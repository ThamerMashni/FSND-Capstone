from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from Env import DB_NAME, DB_PASSWORD, DB_PORT, DB_USERNAME, DB_HOST

# database_path = 'postgres://'f'{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://psegadhfymizsj:b8bf63fac5f6b7fd9787abf7c2fbdcae54d6f55a83b98a09c9c89e2b82e2b44c@ec2-3-216-89-250.compute-1.amazonaws.com:5432/ddi969jer2a1s8'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    db.create_all()


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
movies_actors = db.Table('movies_actors',
                         db.Column('movie_id', db.Integer, db.ForeignKey(
                             'movies.id'), primary_key=True),
                         db.Column('actor_id', db.Integer, db.ForeignKey(
                             'actors.id'), primary_key=True)
                         )


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    actors = db.relationship('Actor', secondary=movies_actors,
                             backref=db.backref('movies', lazy=True))

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        actors = self.actors
        formated_actors = []
        for actor in actors:
            formated_actors.append(actor.format())

        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actors': formated_actors
        }


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
