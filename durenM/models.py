from django.db import models
import extsea
from durenM import rpgdb

class Character(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=50) 
    def __unicode__(self):
        return self.name
    def to_extsea(self):
        character = extsea.Character(self.name)
        for attribute in Attribute.objects.filter(owner = self):
            character.add(attribute.to_extsea())
        return character


class Attribute(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(Character)
    level = models.IntegerField()
    exp = models.IntegerField()
    def __unicode__(self):
        return self.name + '@' + self.owner.name
    def to_extsea(self):
        attribute = rpgdb.createl(self.name, self.level)