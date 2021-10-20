from django.db import models

# Create your models here.
class Trunk(models.Model):
    name = models.CharField(max_length = 50)
    
class Room(models.Model):
    name = models.CharField(max_length = 50)

class Soup(models.Model):
    name = models.CharField(max_length = 50)
    
class Activity(models.Model):
    name = models.CharField(max_length = 50)
    activity = models.CharField(max_length = 50)
    approved = models.BooleanField(default=False)