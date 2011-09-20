#coding=utf-8
from django.http import HttpResponse
from kovin.models import Object, Place

def execute(request):
	temp = Place(name='Duren mniejsze', id='sduren')
	temp.save()
	Object(id=0, name='Sala treningowa', action='goto(\'training_room\')', place=temp).save()
	temp = Place(name='Sala treningowa', id='training_room')
	temp.save()
	Object(id=1, name='Wyjście', action='goto(\'sduren\')', place=temp).save()
	Object(id=2, name='Worek treningowy', action='character.attrib[\'hit\'].exp += 1\nbusy(60)', place=temp).save()
	return HttpResponse('Puff!')
