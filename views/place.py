#coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from kovin.models import Object, Place
import extsea
import rpgdb

def look(request):
	if ('user' in request.session):
		user = request.session['user']
		character = user.to_extsea()
		objects = Object.objects.filter(place=user.place)
		context = {
				   'character' : character,
				   'user' : user, 
				   'objects' : objects,
				   'place' : user.place
				   }
		return render_to_response('place.html', context, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login/')

def action(request, id):
	if ('user' in request.session):
		user = request.session['user']
		character = user.to_extsea()
		objects = Object.objects.filter(place=user.place)
		request.session['dialog'] = []
		def start_battle(chars):
			battle = extsea.Battle(chars)
			battle.run()
			if (character.life <= 0):
				raise('gameover')
		def dialog(text):
			'''Create new dialog'''
			request.session['dialog'].append(text)
		def goto(place_id):
			'''Go to specified location'''
			user.place = Place.objects.get(id=place_id)
		context = {
				   'character' : character,
				   'objects' : objects,
				   'place' : user.place,
				   'start_battle' : start_battle,
				   'dialog' : dialog,
				   'goto' : goto,
				   'rpgdb' : rpgdb,
				   }
		result = None
		obj = Object.objects.get(id=id)
		try:
			exec(obj.action) in context
		except str:
			result = HttpResponseRedirect('/gameover/');
		user.from_extsea(character)
		user.save()
		request.session['user'] = user
		if result == None:
			result = look(request)
		request.session['dialog'] = []
		return result
	else:
		return HttpResponseRedirect('/login/')
