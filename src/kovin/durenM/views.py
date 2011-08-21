#coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from durenM.models import Character
import hashlib

def index(request):
    return render_to_response('index.html')

def welcome(request, name):
    return render_to_response('welcome.html', {'name' : name})

def register(request):
    context = {}
    if request.POST:
        is_exists = Character.objects.filter(name=request.POST['name'])
        new_char = Character()
        new_char.name = request.POST['name']
        context['name'] = request.POST['name']
        if is_exists.count() > 0:
            context['error'] = 'Użytkownik istnieje.'
        if len(request.POST['pass']) < 4:
            context['error'] = 'Za krótkie hasło.'
        if request.POST['pass'] != request.POST['pass2']:
            context['error'] = 'Hasła nie zgadzają się.'
        if not('error' in context):
            new_char.password = hashlib.sha224(request.POST['pass']).hexdigest()
            new_char.save()
            return HttpResponseRedirect('/welcome/' + new_char.name)
    
    context.update(csrf(request))
    return render_to_response('register.html', context)