#coding=utf-8
from django.http import HttpResponse
from kovin.models import Object, Place

def execute(request):
	sduren = Place()
	sduren.name = 'Duren mniejsze'
	sduren.id = 'sduren'
	sduren.save()
	return HttpResponse('Puff!')
	
