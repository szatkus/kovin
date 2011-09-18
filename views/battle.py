#coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from kovin.models import Object, Place, BattleLog
import extsea
import rpgdb

def list(request):
	if ('user' in request.session):
		user = request.session['user']
		character = user.to_extsea()
		battles = BattleLog.objects.filter(owner=user)
		context = {
				   'character' : character,
				   'user' : user, 
				   'battles' : battles
				   }
		return render_to_response('battles.html', context, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login/')

def view(request, id):
	if ('user' in request.session):
		user = request.session['user']
		character = user.to_extsea()
		battle = BattleLog.objects.get(id=id)
		lines = battle.log.split('\n')
		log = []
		for line in lines:
			data = line.split(' ')
			if data[0] == 'use':
				attribute = rpgdb.create(data[1])
				data[1] = attribute.title
			log.append(data)
		context = {
				   'character' : character,
				   'user' : user, 
				   'log' : log
				   }
		return render_to_response('battle.html', context, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login/')
