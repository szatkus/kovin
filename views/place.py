#coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from kovin.models import Object, Place

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
        context = {
                   'character' : character,
                   'user' : user, 
                   'objects' : objects,
                   'place' : user.place
                   }
        object = Object.objects.get(id=id)
        exec(object.action) in context
        user.from_extsea(character)
        user.save()
        request.session['user'] = user
        result = look(request)
        user.dialog_buffer = []
        return result
    else:
        return HttpResponseRedirect('/login/')