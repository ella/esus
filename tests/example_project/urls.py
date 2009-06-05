from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
from django.contrib.auth.views import login, logout

admin.autodiscover()


urlpatterns = patterns('',
    (r'^', include('esus.phorum.urls')),

    url(r'^accounts/registration/', 'helper_test_app.views.registration', name='user-registration'),
    url(r'^accounts/profile/$', 'helper_test_app.views.profile', name='user-profile'),
    url(r'^accounts/login/$',  login, name='user-login'),
    url(r'^accounts/logout/$', logout, name='user-logout'),

    (r'^admin/(.*)', admin.site.root),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT, 'show_indexes': True }),

)

