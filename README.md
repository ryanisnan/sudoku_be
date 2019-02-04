# ryanisnan/sudoku_be

This app is a django backend application that provides an API for completing games of Sudoku. It is a dummy project proving interaction between microservices over a REST API.

# Running locally
```
git clone git@github.com:ryanisnan/sudoku_be.git
cd sudoku_be/src
docker-compose up --build
```

You will then need to run the migrations against your local database.
```
docker exec -it sudoku_be python manage.py migrate
```

To create a dummy game, you can run the provided management command.
```
docker exec -it sudoku_be python manage.py create_game
```


# The API
- /api/v1/games/<int:pk>/
- /api/v1/moves/

## /api/v1/games/<int:pk>/

This endpoint prints to users the status of a game, specified by the pk in the URL. It allows for JSON printing of the game in its current state, resetting of the game board, and "pretty" printing the sudoku board.

**Method:** `GET`
**Query Parameters**
- `pretty=1` - Will return a `text/plain` response with a printout of the game board in its current state. Useful for debugging.
**Request Body:** None
**Response:**
- `200` - Here's your game
- `404` - Game couldn't be found.
- `500` - I broke something.

**Example regular output**
```
[[null,2,null,6,null,8,null,null,null],[5,8,null,null,null,9,7,null,null],[null,null,null,null,4,null,null,null,null],[3,7,null,null,null,null,5,null,null],[6,null,null,null,null,null,null,null,4],[null,null,8,null,null,null,null,1,3],[null,null,null,null,2,null,null,null,null],[null,null,9,8,null,null,null,3,6],[null,null,null,3,null,6,null,9,null]]
```

**Example pretty output**
```
-------------------------------
| 1  2  3 | 6     8 | 1  1  2 |
| 5  8    |       9 | 7  1  3 |
| 6  2    |    4    |       4 |
|-----------------------------|
| 3  7    |         | 5       |
| 6       |         |    5  4 |
|       8 |         |    1  3 |
|-----------------------------|
| 9       |    2    |    1    |
|       9 | 8       |    3  6 |
|         | 3     6 |    9    |
-------------------------------
```

**Method:** `POST`
**Query Parameters**
- `reset` - Supply `true` if you would like to reset the given game board. This is irreversible.
**Request Body:** None
**Response:**
- `200` - The board game you specfied has been reset
- `404` - The game you specified couldn't be found.
- `500` - I broke something.

## /api/v1/moves/

This endpoint allows for the listing of moves that have been made against a given game of Sudoku. This feature theoretically allows for the user to undo previous moves, though after building it I'm not so certain it's entirely useful.

**Method:** `GET`
**Query Parameters**
- `game=<pk>` - **REQUIRED** - Will return a `json` response with the moves that have been made in a game of Sudoku.
**Request Body:** None
**Response:**
- `200` - Here's your move list.
- `404` - Game couldn't be found.
- `500` - I broke something.

**Method:** `POST`
**Query Parameters:** None
**Request Body:**
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

# Todo
[ ] Authentication and authorization
[ ] Sudoku board generation
[ ] Testing facilities
[ ] Pagination on moves endpoint
