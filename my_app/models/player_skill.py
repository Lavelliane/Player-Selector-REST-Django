## /////////////////////////////////////////////////////////////////////////////
## PLEASE DO NOT RENAME OR REMOVE ANY OF THE CODE BELOW. 
## YOU CAN ADD YOUR CODE TO THIS FILE TO EXTEND THE FEATURES TO USE THEM IN YOUR WORK.
## /////////////////////////////////////////////////////////////////////////////

from django.db import models


from .player import Player

class PlayerSkill(models.Model):
    player = models.ForeignKey(Player, related_name='playerSkills', on_delete=models.CASCADE)
    skill = models.CharField(max_length=16, blank=False)
    value = models.IntegerField()
