import random
import math


def get_neighbors(row, col, tiles):
    neighbors = []
    neighbors.extend(tiles[row])
    neighbors.extend([x[col] for x in tiles])

    row_start = int(math.floor(row / 3.0)) * 3
    row_end = row_start + 3

    col_start = int(math.floor(col / 3.0)) * 3
    col_end = col_start + 3

    for _row in tiles[row_start:row_end]:
        neighbors.extend(_row[col_start:col_end])

    neighbors = filter(lambda x: x is not None, neighbors)
    return set(neighbors)


OPTIONS = set(range(1, 10))


def generate_sudoku_tiles(tiles=None):
    """
    TEMP METHOD - DOESN'T QUITE WORK YET
    """
    if tiles is None:
        tiles = [[None for x in range(9)] for y in range(9)]

    for row in range(0, 9):
        for col in range(0, 9):
            # Skip cells that already have a value
            if tiles[row][col] is not None:
                continue

            # Print our board for visual purposes
            print('Board:')
            print('----' * 9)
            for i, x in enumerate(tiles):
                print('| %s |' % ' | '.join([str(y) if y is not None else ' ' for y in x]))

                if i in [2, 5]:
                    print('----' * 9)
            print('----' * 9)

            neighbors = get_neighbors(row, col, tiles)
            valid_options = list(OPTIONS - neighbors)

            # Recursively try all of our valid options
            for option in valid_options:
                tiles[row][col] = option

                if row == 8 and col == 8:
                    return tiles

                return generate_sudoku_tiles(tiles)

            # Base-case, where we've walked into a trap, exit this recursive-branch
            if not valid_options:
                tiles[row][col] = None
                return False
