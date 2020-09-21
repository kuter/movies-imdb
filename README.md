[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

### Task

We'd like you to build simple REST API for us - a basic movie database interacting with external API.
Here's full specification of endpoints that we'd like it to have:
* POST /api/movies:
    - Request body should contain only movie title, and its presence should be validated.
    - Based on passed title, other movie details should be fetched from http://www.omdbapi.com/ (or other similar, public movie database) - and saved to application database.
    - Request response should include full movie object, along with all data fetched from external API.
* GET /api/movies:
    - Should fetch list of all movies already present in application database.
    - Additional filtering, sorting is fully optional - but some implementation is a bonus
* POST /api/comments:
    - Request body should contain ID of movie already present in database, and comment text body.
    - Comment should be saved to application database and returned in request response.
* GET /api/comments:
    - Should fetch list of all comments present in application database.
    - Should allow filtering comments by associated movie, by passing its ID.
* GET /api/top:
    - Should return top movies already present in the database ranking based on a number of comments added to the movie (as in the example) in the specified date range. The response should include the ID of the movie, position in rank and total number of comments (in the specified date range).
    - Movies with the same number of comments should have the same position in the ranking.
    - Should require specifying a date range for which statistics should be generated.
    ### Example response:
    ```json
    [
        {
            "movie_id": 2,
            "total_comments": 4,
            "rank": 1
        },
        {
            "movie_id": 3,
            "total_comments": 2,
            "rank": 2
        },
        {
            "movie_id": 4,
            "total_comments": 2,
            "rank": 2
        },
        {
            "movie_id": 1,
            "total_comments": 0,
            "rank": 3
        }
    ]
    ```

## Running project

```
$ docker-compose up web
```

## Run migrations

```
$ docker-compose run web python manage.py migrate
```

## Running tests

```
$ docker-compose up test
```

## Open project in browser

```
$ xdg-open http://localhost:8000
```
