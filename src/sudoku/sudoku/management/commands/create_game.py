from django.core.management.base import BaseCommand
from sudoku.models import Game


class Command(BaseCommand):
    help = 'Creates a dummy sudoku board.'

    def handle(self, *args, **options):
        tiles = [
            [1, 2, 3, 6, 7, 8, 9, 4, 5],
            [5, 8, 4, 2, 3, 9, 7, 6, 1],
            [9, 6, 7, 1, 4, 5, 3, 2, 8],
            [3, 7, 2, 4, 6, 1, 5, 8, 9],
            [6, 9, 1, 5, 8, 3, 2, 7, 4],
            [4, 5, 8, 7, 9, 2, 6, 1, 3],
            [8, 3, 6, 9, 2, 4, 1, 5, 7],
            [2, 1, 9, 8, 5, 7, 4, 3, 6],
            [7, 4, 5, 3, 1, 6, 8, 9, 2],
        ]

        masked_tiles = [
            [1, 0, 1, 0, 1, 0, 1, 1, 1],
            [0, 0, 1, 1, 1, 0, 0, 1, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 1],
            [0, 0, 1, 1, 1, 1, 0, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 0, 1, 1, 1, 1, 0, 0],
            [1, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 1, 0, 0, 1, 1, 1, 0, 0],
            [1, 1, 1, 0, 1, 0, 1, 0, 1],
        ]

        user_input = [[None for j in range(0, 9)] for i in range(0, 9)]

        game = Game.objects.create(tiles=tiles, masked_tiles=masked_tiles, user_input=user_input, user_id=1)
        print('Created game %d' % game.id)
