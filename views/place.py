#coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from kovin.models import Object, Place, BattleLog, Variable
import extsea
import rpgdb
from datetime import *
from random import random

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
		if user.available > datetime.now():
			context['minutes'] = int((user.available-datetime.now()).total_seconds()/60)+1
			return render_to_response('busy.html', context, context_instance=RequestContext(request))
		response =  render_to_response('place.html', context, context_instance=RequestContext(request))
		request.session['dialog'] = []
		return response
	else:
		return HttpResponseRedirect('/login/')

def action(request, id):
	if ('user' in request.session):
		user = request.session['user']
		character = user.to_extsea()
		objects = Object.objects.filter(place=user.place)
		request.session['dialog'] = []
		def dialog(text):
			'''Create new dialog'''
			request.session['dialog'].append(text)
		def start_battle(chars):
			'''Start new battle'''
			text = 'Walka: '
			for c in chars:
				text += c.name+', '
			battle = extsea.Battle(chars)
			battle.run()
			log = BattleLog(log='\n'.join(battle.log), owner=user)
			log.save()
			text += '<a href="/battle/'+str(log.id)+'">Zobacz</a>'
			dialog(text)
			if (character.life <= 0):
				raise(Exception('gameover'))
		def goto(place_id):
			'''Go to specified location'''
			user.place = Place.objects.get(id=place_id)
		def busy(delta):
			'''Make player busy for x minutes'''
			user.available = datetime.now()+timedelta(minutes=delta)
		def chance(p):
			return(random() <= p)
		def receive(name, amount):
			item = rpgdb.createl(name, amount)
			text = 'Zdobyłeś '+item.title
			if amount > 1:
				text += ' (' + str(amount) + ')'
			dialog(text)
			character.add(item)
		def stop():
			raise(Exception('stop'))
		context = {
				   'character' : character,
				   'objects' : objects,
				   'place' : user.place,
				   'start_battle' : start_battle,
				   'dialog' : dialog,
				   'goto' : goto,
				   'rpgdb' : rpgdb,
				   'vardb' : Variable,
				   'busy' : busy,
				   'chance' : chance,
				   'receive' : receive,
				   'stop' : stop,
				   }
		result = None
		if user.available > datetime.now():
			context['minutes'] = int((user.available-datetime.now()).total_seconds()/60)+1
			return render_to_response('busy.html', context, context_instance=RequestContext(request))
		obj = Object.objects.get(place=user.place, id=id)
		try:
			exec(obj.action) in context
		except Exception as e:
			if e.message != 'stop':
				if e.message == 'gameover':
					result = HttpResponseRedirect('/gameover/')
				else:
					raise(e)
		user.from_extsea(character)
		user.save()
		request.session['user'] = user
		if result == None:
			result = HttpResponseRedirect('/place/')
		return result
	else:
		return HttpResponseRedirect('/login/')
