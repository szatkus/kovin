#coding=utf-8
from django.http import HttpResponse
from kovin.models import Object, Place
import os

def execute(request):
	places = Place.objects.all()
	output = open('generate_db.py', 'w+')
	output.write('#coding=utf-8\nfrom django.http import HttpResponse\nfrom kovin.models import Object, Place\n\ndef execute(request):\n')
	for place in places:
		output.write('\ttemp = Place(name=\''+place.name+'\', id=\''+place.id+'\')\n');
		output.write('\ttemp.save()\n')
		objects = Object.objects.filter(place=place)
		for obj in objects:
			obj.action = obj.action.replace('\n', '\\n')
			obj.action = obj.action.replace('\'', "\\'")
			text = ('\tObject(id='+str(obj.id+10000)+', name=\''+obj.name+'\', action=\''+obj.action+'\', place=temp).save()\n')
			
			output.write(text.encode('UTF-8'))
	output.write('\treturn HttpResponse(\'Puff!\')')
	output.close()
	return HttpResponse('Puff!')
	
