## /////////////////////////////////////////////////////////////////////////////
## YOU CAN FREELY MODIFY THE CODE BELOW IN ORDER TO COMPLETE THE TASK
## /////////////////////////////////////////////////////////////////////////////

from django.http.response import JsonResponse
from rest_framework.request import Request
from rest_framework import status
from typing import Any
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from my_app.models import Player
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def delete_player_handler(request: Request, id: Any):
    # Check if Authorization header is present
    if 'Authorization' not in request.headers:
        return JsonResponse({'error': 'Authorization header missing'}, status=status.HTTP_401_UNAUTHORIZED)

    # Check if Authorization header has the correct token
    auth_header = request.headers['Authorization']
    expected_token = "SkFabTZibXE1aE14ckpQUUxHc2dnQ2RzdlFRTTM2NFE2cGI4d3RQNjZmdEFITmdBQkE="
    if auth_header != f"Bearer {expected_token}":
        return JsonResponse({'error': 'Invalid authorization token'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        player = Player.objects.get(id=id)
        player.delete()
        return JsonResponse({'success': True})
    except Player.DoesNotExist:
        return JsonResponse({'error': f'Player with id {id} does not exist'}, status=status.HTTP_404_NOT_FOUND)

