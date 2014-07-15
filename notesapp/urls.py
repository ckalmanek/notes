from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns  import format_suffix_patterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('notesapp.views',
    # Examples:
    # url(r'^$', 'notes.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^notesapp/$', 'note_list'),
    url(r'^notesapp/(?P<pk>[0-9]+)/$', 'note_detail'),
    # url(r'^users/$', 'user_list'),
    # url(r'^users/(?P<pk>[0-9]+)/$', 'user_detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
