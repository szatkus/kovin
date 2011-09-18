#coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf

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
