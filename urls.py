from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^login/', 'durenM.views.login'),
    (r'^register/', 'durenM.views.register'),
    (r'^welcome/(?P<name>[a-zA-Z_]+)', 'durenM.views.welcome'),
    (r'^$', 'durenM.views.index'),
)
