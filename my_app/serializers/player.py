from rest_framework import serializers 

from .player_skill import PlayerSkillSerializer
from ..models.player import Player
from ..models.player_skill import PlayerSkill

class PlayerSerializer(serializers.ModelSerializer):
    playerSkills = PlayerSkillSerializer(many=True)

    class Meta:
        model = Player
        fields = ['id', 'name', 'position', 'playerSkills']

    def create(self, validated_data):
        player_skills_data = validated_data.pop('playerSkills')
        player = Player.objects.create(**validated_data)
        for skill_data in player_skills_data:
            PlayerSkill.objects.create(player=player, **skill_data)
        return player
    def validate_position(self, value):
        valid_positions = ['defender', 'midfielder', 'forward']
        if value not in valid_positions:
            raise serializers.ValidationError("Invalid value for position: {}".format(value))
        return value
    def update(self, instance, validated_data):
        # Update Player fields
        instance.name = validated_data.get('name', instance.name)
        instance.position = validated_data.get('position', instance.position)

        # Update or create PlayerSkill instances
        player_skills_data = validated_data.pop('playerSkills', [])
        existing_player_skills = {player_skill.id: player_skill for player_skill in instance.playerSkills.all()}
        for player_skill_data in player_skills_data:
            player_skill_id = player_skill_data.get('id', None)
            if player_skill_id is not None and player_skill_id in existing_player_skills:
                # Update existing PlayerSkill instance
                player_skill = existing_player_skills[player_skill_id]
                player_skill.skill = player_skill_data.get('skill', player_skill.skill)
                player_skill.value = player_skill_data.get('value', player_skill.value)
                player_skill.save()
            else:
                # Create new PlayerSkill instance
                player_skill = PlayerSkill(player=instance, **player_skill_data)
                player_skill.save()
                
        # Delete any PlayerSkill instances that were not included in the updated data
        for player_skill_id, player_skill in existing_player_skills.items():
            if player_skill_id not in [player_skill_data.get('id') for player_skill_data in player_skills_data]:
                player_skill.delete()

        instance.save()
        instance.refresh_from_db()
        return instance