from django.http import JsonResponse
from django.views.generic import View
from ...models import Game


class GameAPIViewV1(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'message': 'You must be authenticated to list games.'}, status=401)

        games = Game.objects.filter(user=request.user)
        games_serialized = [x.to_dict() for x in games]

        return JsonResponse({'games': games_serialized}, status=200)
