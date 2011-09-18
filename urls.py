from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from kovin import views
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^login/', views.user.login),
    (r'^logout/', views.user.logout),
    (r'^register/', views.user.register),
    (r'^welcome/(?P<name>[a-zA-Z_]+)', views.user.welcome),
    (r'^stats/ex', views.character.stats_ex),
    (r'^stats/', views.character.stats),
    (r'^place/$', views.place.look),
    (r'^place/(?P<id>\d+)', views.place.action),
    (r'^gameover/', views.user.gameover),
    (r'^generate_db/', views.generate_db.execute),
    (r'^battles/', views.battle.list),
    (r'^battle/(?P<id>\d+)', views.battle.view),
    (r'^$', views.user.index),
)
