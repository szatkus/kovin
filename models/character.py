from django.db import models
from place import Place
import extsea
import rpgdb

class Character(models.Model):
	'''Character class for django'''
	name = models.CharField(max_length=50, primary_key=True)
	password = models.CharField(max_length=100)
	place = models.ForeignKey(Place)
	available = models.DateTimeField()
	class Meta:
		app_label = 'kovin'
	def __unicode__(self):
		return self.name
	def to_extsea(self):
		'''Convert django model into character from extsea module'''
		character = extsea.Character(self.name)
		for attribute in Attribute.objects.filter(owner = self, disabled = False):
			character.add(attribute.to_extsea())
		character.fight = rpgdb.ai_custom
		return character
	@staticmethod
	def from_extsea(character):
		'''Create django model from extsea character'''
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
	'''Single attribute'''
	name = models.CharField(max_length=50)
	owner = models.ForeignKey(Character)
	level = models.IntegerField()
	exp = models.FloatField()
	disabled = models.BooleanField()
	class Meta:
		app_label = 'kovin'
	def __unicode__(self):
		return self.name + '@' + self.owner.name
	def to_extsea(self):
		'''Convert into extsea class'''
		attribute = rpgdb.createl(self.name, self.level)
		attribute.id = self.id
		attribute.rlevel = attribute.level
		attribute.exp = self.exp
		return attribute
	@staticmethod
	def from_extsea(attribute):
		'''Create new model from extsea object'''
		if hasattr(attribute, 'id'):
			attribute_model = Attribute.objects.get(id=attribute.id)
		else:
			attribute_model = Attribute()
		attribute_model.name = attribute.name
		attribute_model.level = attribute.rlevel
		attribute_model.exp = attribute.exp
		return attribute_model
