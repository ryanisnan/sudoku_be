from ...models import Game
from django.http import Http404
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
        return Response(game.tiles, status=status.HTTP_200_OK)
