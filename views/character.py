#coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf
from kovin.models import Attribute

def stats(request):
	if ('user' in request.session):
		user = request.session['user']
		character = user.to_extsea()
		return render_to_response('stats.html', {'character' : character}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login/')

def stats_ex(request):
	if ('user' in request.session):
		user = request.session['user']
		character = user.to_extsea()
		return render_to_response('stats_ex.html', {'character' : character}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login/')

def list(request, atype):
	if ('user' in request.session):
		user = request.session['user']
		character = user.to_extsea()
		trash = []
		for attribute in Attribute.objects.filter(disabled=True):
			trash.append(attribute.to_extsea())
		context = {
			'character' : character,
			'trash' : trash,
			'atype' : atype
		}
		return render_to_response('list.html', context, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login/')

def disable(request, name):
	if ('user' in request.session):
		user = request.session['user']
		attribute = Attribute.objects.get(name=name, owner=user)
		attribute.disabled = True
		attribute.save()
		atype = attribute.to_extsea().atype
		return HttpResponseRedirect('/list/' + atype)
	else:
		return HttpResponseRedirect('/login/')

def enable(request, name):
	if ('user' in request.session):
		user = request.session['user']
		attribute = Attribute.objects.get(name=name, owner=user)
		attribute.disabled = False
		attribute.save()
		atype = attribute.to_extsea().atype
		return HttpResponseRedirect('/list/' + atype)
	else:
		return HttpResponseRedirect('/login/')
