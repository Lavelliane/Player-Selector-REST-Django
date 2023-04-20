from rest_framework import serializers 

from ..models.player_skill import PlayerSkill

class PlayerSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerSkill
        fields = ['id', 'skill', 'value']

    def validate_value(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError("Invalid value for value: {}".format(value))
        return value

    def validate_skill(self, value):
        valid_skills = ['defense', 'attack', 'speed', 'strength', 'stamina']
        if value not in valid_skills:
            raise serializers.ValidationError("Invalid value for skill: {}".format(value))
        return value
