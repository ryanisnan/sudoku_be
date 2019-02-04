from ...models import Move
from ...models import Game
from rest_framework import serializers
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


def tile_coordinates(value):
    valid_values = range(0, 9)
    if value not in valid_values:
        raise serializers.ValidationError('Not a valid value.')


def sudoku_value(value):
    valid_values = [None]
    valid_values.extend(range(1, 10))
    if value not in valid_values:
        raise serializers.ValidationError('Not a valid value.')


class MoveSerializer(serializers.ModelSerializer):
    x = serializers.IntegerField(validators=[tile_coordinates])
    y = serializers.IntegerField(validators=[tile_coordinates])
    value = serializers.IntegerField(validators=[sudoku_value])

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

            # Ensure the tile can be edited
            if not game.is_tile_editable(serializer.validated_data.get('x'), serializer.validated_data.get('y')):
                return Response({'detail': 'The given coordinate is not editable.'}, status=status.HTTP_400_BAD_REQUEST)

            # TODO: Ensure that value satisfies the game rules

            # Determine the last move dynamically
            previous_move = Move.objects.filter(game=request.data.get('game')).order_by('-id').first()
            serializer.save(previous_move=previous_move)

            # Update the game state
            game.user_input[serializer.validated_data['x']][serializer.validated_data['y']] = serializer.validated_data['value']
            game.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
