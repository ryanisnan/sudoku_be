from django.contrib import admin
from .models import Game
from .models import Move


class MoveAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'x', 'y', 'value')
    list_filter = ('game',)


admin.site.register(Move, MoveAdmin)
admin.site.register(Game)
