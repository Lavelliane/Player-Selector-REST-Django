## /////////////////////////////////////////////////////////////////////////////
## YOU CAN FREELY MODIFY THE CODE BELOW IN ORDER TO COMPLETE THE TASK
## /////////////////////////////////////////////////////////////////////////////

from django.http.response import JsonResponse
from rest_framework.request import Request
from rest_framework import status

from my_app.models.player import Player
from my_app.serializers.player import PlayerSerializer

def get_player_list_handler(request: Request):
    try:
        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)
        return JsonResponse({'players': serializer.data})
    except Exception:
        return JsonResponse('', status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
