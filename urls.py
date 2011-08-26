from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from kovin import views
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^login/', views.login),
    (r'^logout/', views.logout),
    (r'^register/', views.register),
    (r'^welcome/(?P<name>[a-zA-Z_]+)', views.welcome),
    (r'^stats/', views.character.stats),
    (r'^$', views.index),
)
