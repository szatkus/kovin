#coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf
from kovin.models import Character, Place
import extsea
import re
import hashlib
import rpgdb



def index(request):
    if ('user' in request.session):
        user = request.session['user']
        character = user.to_extsea()
        return render_to_response('dashboard.html', {'character' : character}, context_instance=RequestContext(request))
    else:
        return render_to_response('index.html')

def welcome(request, name):
    return render_to_response('welcome.html', {'name' : name})

def register(request):
    context = {}
    if ('user' in request.session):
        return HttpResponseRedirect('/')
    if request.POST:
        pattern = re.compile('^[A-z0-9_]+$')
        if not(pattern.match(request.POST['name'])):
            context['error'] = 'Nieprawidłowe znaki w nazwie użytkownika.'
        is_exists = Character.objects.filter(name=request.POST['name'])
        context['name'] = request.POST['name']
        if is_exists.count() > 0:
            context['error'] = 'Użytkownik istnieje.'
        if len(request.POST['pass']) < 4:
            context['error'] = 'Za krótkie hasło.'
        if request.POST['pass'] != request.POST['pass2']:
            context['error'] = 'Hasła nie zgadzają się.'
        if not('error' in context):
            new_char = extsea.Character(request.POST['name'])
            new_char.add(rpgdb.create("human"))
            new_char.add(rpgdb.createl("strength", 1))
            new_char.add(rpgdb.createl("speed", 1))
            new_char.add(rpgdb.createl("life", 1))
            new_char.add(rpgdb.createl("hit", 1))
            if (request.POST['gender'] == 'male'):
                new_char.add(rpgdb.create('male'))
            else:
                new_char.add(rpgdb.create('female'))
            new_user = Character.from_extsea(new_char)
            new_user.password = hashlib.sha224(request.POST['pass']).hexdigest()
            new_user.place = Place.objects.all()[0]
            new_user.save()
            return HttpResponseRedirect('/welcome/' + new_char.name)
    
    context.update(csrf(request))
    return render_to_response('register.html', context)

def login(request):
    context = {}
    if ('user' in request.session):
        return HttpResponseRedirect('/')
    if request.POST:
        user = Character.objects.filter(name=request.POST['name'])
        password = hashlib.sha224(request.POST['pass']).hexdigest()
        if (user.count() == 0) or (password != user[0].password):
            context['error'] = 'Nie udało się zalogować.'
        else:
            request.session['user'] = user[0]
            return HttpResponseRedirect('/')
        
    
    context.update(csrf(request))
    return render_to_response('login.html', context)

def logout(request):
    if ('user' in request.session):
        del request.session['user']
    return render_to_response('logout.html')
