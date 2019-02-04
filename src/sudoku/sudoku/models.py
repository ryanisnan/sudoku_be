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


class Move(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    previous_move = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    x = models.PositiveSmallIntegerField(help_text='The X coordinate on the board.')
    y = models.PositiveSmallIntegerField(help_text='The Y coordinate on the board.')
    value = models.PositiveSmallIntegerField(blank=True, null=True, help_text='The value the move changes the coordinate to.')
