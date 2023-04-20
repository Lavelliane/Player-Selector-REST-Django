from typing import Dict, Any, List
from django.http import JsonResponse
from rest_framework import status
from rest_framework.request import Request
from my_app import models
from my_app.models.player import Player
from my_app.models.player_skill import PlayerSkill


def team_process_handler(request: Request):
    if request.method == 'POST':
        requirements = request.data
        
        # Rule 3: Check for duplicate position and skill combinations
        position_skill_counts = {}
        for requirement in requirements:
            position = requirement.get('position')
            skill = requirement.get('mainSkill')
            count = position_skill_counts.get(f'{position}-{skill}', 0)
            position_skill_counts[f'{position}-{skill}'] = count + 1
            if count > 0:
                return JsonResponse({'error': f'Duplicate position and skill combination: {position}, {skill}'},
                                    status=status.HTTP_400_BAD_REQUEST)

        # Rule 1: Find the best player for each requirement
        players = []
        for requirement in requirements:
            position = requirement.get('position')
            skill = requirement.get('mainSkill')
            count = requirement.get('numberOfPlayers', 1)

            # Get all players with the desired position
            position_players = Player.objects.filter(position=position)

            # Check if there are players with the desired skill
            skill_players = position_players.filter(playerSkills__skill=skill)

            if skill_players.exists():
                # Get the player(s) with the highest skill value
                max_skill_values = skill_players.values_list('playerSkills__value', flat=True).order_by('-playerSkills__value')[:2]
                skill_players = skill_players.filter(playerSkills__value__in=max_skill_values)
            else:
                # Rule 4: Get the player with the highest skill value for the desired position
                max_skill_value = position_players.aggregate(models.Max('playerSkills__value'))['playerSkills__value__max']
                skill_players = position_players.filter(playerSkills__value=max_skill_value)


            if not skill_players.exists():
                # Rule 6: Return an error if there are no available players in the required position
                return JsonResponse({'error': f'Insufficient number of players for position: {position}'},
                                    status=status.HTTP_400_BAD_REQUEST)

            # Add the best player(s) for the requirement to the list
            players.extend(skill_players.order_by('?')[:count])

        # Remove any duplicates
        players = list(set(players))

        # Rule 5: Fill the number of required players with the correct position
        final_players = []
        for requirement in requirements:
            position = requirement.get('position')
            count = requirement.get('numberOfPlayers', 1)
            selected_players = [p for p in players if p.position == position][:count]
            final_players.extend(selected_players)

        # Serialize the players and return the response
        data = []
        for player in final_players:
            serialized_player = {
                'name': player.name,
                'position': player.position,
                'playerSkills': []
            }
            skills = player.playerSkills.all()
            for skill in skills:
                serialized_skill = {
                    'skill': skill.skill,
                    'value': skill.value
                }
                serialized_player['playerSkills'].append(serialized_skill)
            data.append(serialized_player)
        return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
