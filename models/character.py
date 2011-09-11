from django.db import models
from place import Place
import extsea
import rpgdb

'''Character class for django'''
class Character(models.Model):
	name = models.CharField(max_length=50, primary_key=True)
	password = models.CharField(max_length=100)
	place = models.ForeignKey(Place)
	dialog_buffer = []
	class Meta:
		app_label = 'kovin'
	def __unicode__(self):
		return self.name
	'''Create new dialog'''
	def dialog(self, text):
		self.dialog_buffer.append(text)
	'''Go to specified location'''
	def goto(self, place_id):
		self.place = Place.objects.get(id=place_id)
	'''Convert django model into character from extsea module'''
	def to_extsea(self):
		character = extsea.Character(self.name)
		for attribute in Attribute.objects.filter(owner = self):
			character.add(attribute.to_extsea())
		def fight(char, battle):
			target = char
			i = 0
			while target == char:
				target = battle.char[i]
				i = i+1
			hit = char.attrib['hit']
			hit.use(hit, char, target)
			print(target.name)
		character.fight = fight
		return character
	'''Create django model from extsea character'''
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

'''Single attribute'''
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
		attribute.rlevel = attribute.level
		attribute.exp = self.exp
		return attribute
	@staticmethod
	def from_extsea(attribute):
		if hasattr(attribute, 'id'):
			attribute_model = Attribute.objects.get(id=attribute.id)
		else:
			attribute_model = Attribute()
		attribute_model.name = attribute.name
		attribute_model.level = attribute.rlevel
		attribute_model.exp = attribute.exp
		return attribute_model
