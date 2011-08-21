from django.db import models

class Character(models.Model):
    name = models.CharField(max_length=50)


class Attribute(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(Character)
    level = models.IntegerField()
    exp = models.IntegerField()