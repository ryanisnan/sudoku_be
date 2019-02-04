from ...models import Game
from django.http import Http404
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class GameAPIDetailViewV1(APIView):
    def get(self, request, pk, format=None):

        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            raise Http404

        '''
        Response:
        {
            tiles: [
                [], // Row 1
                [], // Row 2
                [], // Row 3

                [], // Row 4
                [], // Row 5
                [], // Row 6

                [], // Row 7
                [], // Row 8
                [], // Row 9
            ]
        }
        '''
        rendered_game = game.tiles

        if request.GET.get('pretty', False):
            output = '-' + '---' * 9 + '---\n'
            for i, row in enumerate(rendered_game):
                output += '|'
                for j, tile in enumerate(row):
                    output += ' %s ' % tile if tile >= 0 else ' '
                    if j in [2, 5]:
                        output += '|'
                output += '|\n'

                # Separator between every 3 rows
                if i in [2, 5]:
                    output += '|' + '---' * 9 + '--|\n'

            output += '-' + '---' * 9 + '---\n'
            return HttpResponse(output, status=status.HTTP_200_OK, content_type='text/plain')

        return Response(game.tiles, status=status.HTTP_200_OK)
