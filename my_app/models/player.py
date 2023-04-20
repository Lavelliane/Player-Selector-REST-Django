## /////////////////////////////////////////////////////////////////////////////
## PLEASE DO NOT RENAME OR REMOVE ANY OF THE CODE BELOW. 
## YOU CAN ADD YOUR CODE TO THIS FILE TO EXTEND THE FEATURES TO USE THEM IN YOUR WORK.
## /////////////////////////////////////////////////////////////////////////////

from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=64, blank=False, default='')
    position = models.CharField(max_length=16, blank=False)
