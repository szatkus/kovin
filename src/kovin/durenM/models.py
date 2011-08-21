from django.db import models

class Character(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    def __unicode__(self):
        return self.name


class Attribute(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(Character)
    level = models.IntegerField()
    exp = models.IntegerField()
    def __unicode__(self):
        return self.name + '@' + self.owner.name