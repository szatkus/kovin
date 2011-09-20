#coding=utf-8
from django.http import HttpResponse
from kovin.models import Object, Place

def execute(request):
	sduren = Place()
	sduren.name = 'Duren mniejsze'
	sduren.id = 'sduren'
	sduren.save()
	Object(id=10000,name='Sala treningowa', action='goto(\'training_room\')', place=sduren).save()
	temp = Place(name='Sala treningowa', id='training_room')
	temp.save()
	Object(id=10001,name='Wyjście', action='goto(\'sduren\')', place=temp).save()
	Object(id=10002,name='Worek treningowy', action='character.attrib[\'hit\'].exp += 1\nbusy(60)', place=temp).save()
	return HttpResponse('Puff!')
	
