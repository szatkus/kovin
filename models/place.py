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