from ...models import Move
from ...models import Game
from rest_framework import serializers
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class MoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Move
        fields = ('id', 'game', 'previous_move', 'x', 'y', 'value')
        read_only_fields = ('id', 'previous_move',)


class MoveAPIListViewV1(APIView):
    def get(self, request, format=None):
        game_id = request.GET.get('game', None)
        try:
            game_id = int(game_id)
        except (TypeError, ValueError):
            return Response({'detail': 'The query parameter game must be a positive integer.'}, status.HTTP_400_BAD_REQUEST)

        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            raise Http404

        moves = Move.objects.filter(game=game)
        serializer = MoveSerializer(moves, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MoveSerializer(data=request.data)
        if serializer.is_valid():
            game = serializer.validated_data.get('game')
            if not game.is_tile_editable(serializer.validated_data.get('x'), serializer.validated_data.get('y')):
                return Response({'detail': 'The given coordinate is not editable.'}, status=status.HTTP_400_BAD_REQUEST)

            # TODO: Ensure that value satisfies the game rules

            # Determine the last move dynamically
            previous_move = Move.objects.filter(game=request.data.get('game')).order_by('-id').first()
            serializer.save(previous_move=previous_move)

            # TODO: Update the game state

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
