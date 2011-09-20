from django.db import models

class Place(models.Model):
	name = models.CharField(max_length=50)
	id = models.CharField(max_length=50, primary_key=True)
	class Meta:
		app_label = 'kovin'
		verbose_name = 'miejsce'
		verbose_name_plural = 'miejsca'
	def __unicode__(self):
		return self.name
	
class Object(models.Model):
	name = models.CharField(max_length=50)
	action = models.CharField(max_length=2000, blank=True)
	place = models.ForeignKey(Place)
	class Meta:
		app_label = 'kovin'
		verbose_name = 'obiekt'
		verbose_name_plural = 'obiekty'
	def __unicode__(self):
		return self.name + ' w ' + self.place.name

class Variable(models.Model):
	key = models.CharField(max_length=50, primary_key=True)
	value = models.CharField(max_length=50)
	class Meta:
		app_label = 'kovin'
	def __unicode__(self):
		return self.key
	@staticmethod
	def set(key, value):
		variable = Variable.objects.get_or_create(key=key)[0]
		variable.value = str(value)
		variable.save()
	@staticmethod
	def get(key):
		variable = Variable.objects.filter(key=key)
		if variable.count() > 0:
			return variable[0].value
		return None
	@staticmethod
	def getb(key):
		return Variable.get(key) == 'True'
	@staticmethod
	def tick(key):
		Variable.set(key, True)
