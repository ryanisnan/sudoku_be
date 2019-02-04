from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Values of the tiles, possibly unknown to the user
    tiles = ArrayField(
        ArrayField(
            models.PositiveSmallIntegerField(blank=True, null=True),
            size=9,
        ),
        size=9,
    )

    # What tiles are opaque to the user on start
    masked_tiles = ArrayField(
        ArrayField(
            models.BooleanField(default=True),
            size=9,
        ),
        size=9,
    )

    # What the user has input
    user_input = ArrayField(
        ArrayField(
            models.PositiveSmallIntegerField(blank=True, null=True),
            size=9,
        ),
        size=9,
    )

    def render_game(self):
        # Produce a 2-D array of the board, masking the hidden tile values, and
        # filling in what the user has entered.
        rendered_game = self.tiles

        # Hide masked tiles
        # TODO: Using a lib like numpy to do matrix masking would be more efficient.
        for i, masked_row in enumerate(self.masked_tiles):
            for j, masked_tile in enumerate(masked_row):
                if masked_tile:
                    rendered_game[i][j] = None

        # Overlay user input
        for i, input_row in enumerate(self.user_input):
            for j, input_tile in enumerate(input_row):
                is_editable = bool(rendered_game[i][j] is None)
                if is_editable:
                    rendered_game[i][j] = input_tile

        return rendered_game

    def is_tile_editable(self, x, y):
        # A tile is considered editable if it has been masked
        return bool(self.masked_tiles[x][y])


class Move(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    previous_move = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    x = models.PositiveSmallIntegerField(help_text='The X coordinate on the board.')
    y = models.PositiveSmallIntegerField(help_text='The Y coordinate on the board.')
    value = models.PositiveSmallIntegerField(blank=True, null=True, help_text='The value the move changes the coordinate to.')
