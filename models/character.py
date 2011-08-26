from django.db import models
import extsea
import rpgdb

class Character(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=50)
    class Meta:
        app_label = "kovin"
    def __unicode__(self):
        return self.name    
    def to_extsea(self):
        character = extsea.Character(self.name)
        for attribute in Attribute.objects.filter(owner = self):
            character.add(attribute.to_extsea())
        return character
    @staticmethod
    def from_extsea(character):
        result = Character.objects.filter(name=character.name)
        if len(result) > 0:
            character_model = result[0]
        else:
            character_model = Character()
            character_model.name = character.name
        for i in character.attrib:
            attribute = Attribute.from_extsea(character.attrib[i])
            attribute.owner_id = character_model
            attribute.save()
        return character_model

class Attribute(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(Character)
    level = models.IntegerField()
    exp = models.IntegerField()
    class Meta:
        app_label = 'kovin'
    def __unicode__(self):
        return self.name + '@' + self.owner.name
    def to_extsea(self):
        attribute = rpgdb.createl(self.name, self.level)
        attribute.id = self.id
        return attribute
    @staticmethod
    def from_extsea(attribute):
        if hasattr(attribute, 'id'):
            attribute_model = Attribute.object.get(id=attribute.id)
        else:
            attribute_model = Attribute()
            attribute_model.exp = 0
        attribute_model.name = attribute.name
        attribute_model.level = attribute.rlevel
        return attribute_model
