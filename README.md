# Running locally
`docker-compose up --build`
`curl localhost:8000`

# Running the migrations
`docker exec -it sudoku_be python manage.py migrate`

# Creating a superuser
`docker exec -it sudoku_be python manage.py createsuperuser`


# The API

## GET: /api/v1/moves

**Query Parameters**
- `game` - The ID of the game you wish to query moves for

**Response**

TODO

## POST: /api/v1/moves

**Request body**
```
{
    game: 42,
    x: 3,
    y: 5,
    value: 7
}
```

**Response**
- `201` - The move was created successfully. Includes the JSON representation of the move.
- `400` - There was a problem with your request.
- `404` - The game you are trying to create a move for wasn't found.
