# FSND-Capstone
This project is the final project for my Udacity FullStack Developer Nanodegree.

## API Link
https://fsnd-capstone-mashni.herokuapp.com/

## Working with the application locally
Make sure you have [Python](https://www.python.org/downloads/) installed.

1. **Clone the Repository**
    ```bash
    git clone -b master https://github.com/cynepton/fsnd-capstone.git
    ```

2. **Set up a virtual environment**:
    ```bash
    virtualenv env
    source env/Scripts/activate # for windows
    source env/bin/activate # for MacOs
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Export Environment Variables**
    Refer to the `setup.bash` file and export the environment variables for the project.

5. **Create Local Database**:
    Create a local database and export the database URI as an environment variable with the key `DATABASE_PATH`.

6. **Run Database Migrations**:
    ```bash
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    ```

7. **Run the Flask Application locally**:
    ```bash
    export FLASK_APP=myapp
    export FLASK_ENV=development
    flask run
    ```
## Roles and Permissions
The application has 3 roles setup:

1. **Casting Assistant**
    - Can *get* all actors in the database
    - Can *get* all movies in the database

2. **Casting Director**
    - *All permissions* of the casting assistant
    - Can *post* a new actor
    - Can *modify* the details of an existing actor
    - Can *delete* an actor from the database
    - Can *modify* the details of an existing movie

3. **Executive Producer**
    - *All permissions* of the casting director
    - Can *post* a new movie
    - Can *delete* a movie from the database

## Endpoints
### Index `/`
Endpoint that indicates the application is running normally
**Response**:<br>
- Require roles: no, public 
- Type: JSON
- Body: 
    ```json
    {
        "page": "FSND Capstone Project"
    }
    ```

### Auth `/auth`
Redirects to the Auth0 login page.

### GET `/actors`
Returns list of actors
- Require roles: Casting Assistant or Casting Director or Executive Producer
- Type: JSON
- Body
    ```json
    {
        "actors": [
            {
                "age": 60,
                "gender": "Male",
                "id": 3,
                "name": "Crowe Russell"
            },
            {
                "age": 40,
                "gender": "Female",
                "id": 4,
                "name": "Michelle Williams"
            }
        ],
        "success": true
    }
    ```
### POST `/actors`
To add an actor to the database, It takes new actor details as a JSON body<br>
Request body:
```json
{
    "name": "actor name",
    "age": 33,
    "gender": "gender"
}
```
Response :
```json
{
    "actor": {
        "age": 33,
        "gender": "gender",
        "id": 1,
        "name": "actor name"
    },
    "success": true
}
```
### PATCH `/actors/<int:id>`
Takes actor id in order to updated it, 

Request body:
```json
{
    "name": "actor name",
    "age": 33,
    "gender": "gender"
}
```
Response :
```json
{
    "actor": {
        "age": 33,
        "gender": "gender",
        "id": 1,
        "name": "actor name"
    },
    "success": true
}
```

### DELETE `/actors/<int:id>`
Takes actor id in order to delete it, 

if succeeded to delete the actor the response would be:
```json
{
    "success": "True",
    "deleted": "id"
}
```

### GET `/movies`
Returns list of movies
```json
{
    "movies": [
        {
            "actors": [
                {
                    "age": 60,
                    "gender": "Male",
                    "id": 3,
                    "name": "Crowe Russell"
                },
                {
                    "age": 40,
                    "gender": "Female",
                    "id": 4,
                    "name": "Michelle Williams"
                }
            ],
            "id": 2,
            "release_date": "Sun, 02 Feb 2020 00:00:00 GMT",
            "title": "test movie"
        },
        {
            "actors": [],
            "id": 3,
            "release_date": "Sun, 02 Feb 2020 00:00:00 GMT",
            "title": "test movie"
        }
    ],
    "success": true
}
```
### POST `/movies`
To add a movie to the database, It takes new movie details as a JSON body<br>
Request body:
```json

{
    "title": "test movie",
    "release_date": "02-02-2020",
    "actors": []
}

```
Response :
```json
{
    "movie": "<movie_id>",
    "success": true
}
```
### PATCH `/movies/<int:id>`
Takes movie id in order to updated it, 

Request body:
```json
{
    "title": "movie title"
}
```
Response :
```json
{
    "movie": {
        "actors": [],
        "id": 1,
        "release_date": "Sun, 02 Feb 2020 00:00:00 GMT",
        "title": "movie title"
    },
    "success": true
}
```
### DELETE `/movies/<int:id>`
Takes movie id in order to delete it, 

if succeeded to delete the actor the response would be:
```json
{
    "success": "True",
    "deleted": "id"
}
```

## Testing
To run the tests locally, run
```

dropdb capstone_test
createdb capstone_test
psql capstone_test < capstone_test.psql
python test_app.py
```

To test roles using Postman you can import the json file 
```
FSND-capstone.postman_collection.json
```