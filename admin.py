from django.contrib import admin
from django import forms
from kovin.models import *


class PlaceModelForm(forms.ModelForm):
    action = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Place

class PlaceAdmin(admin.ModelAdmin):
    form = PlaceModelForm


admin.site.register(Character)
admin.site.register(Attribute)
admin.site.register(Place)
admin.site.register(Object, PlaceAdmin)