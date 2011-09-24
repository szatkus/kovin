from django.db import models
import extsea
from character import Character

class BattleLog(models.Model):
	log = models.CharField(max_length=2000)
	owner = models.ForeignKey(Character)
	time = models.DateTimeField(auto_now_add=True)
	class Meta:
		app_label = 'kovin'
	def __unicode__(self):
		return str(self.id)
	def get_time(self):
		return self.time.strftime('%d %B %Y %H:%M')
