from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns  import format_suffix_patterns
from notesapp import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'notes.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #API endpoints
    
    url(r'^notesapp/$', views.NoteList.as_view(), name='note-list'),
    url(r'^notesapp/(?P<pk>[0-9]+)/$', views.NoteDetail.as_view(), name='note-detail'),
    url(r'^notesapp/(?P<pk>[0-9]+)/comment/$', views.CommentList.as_view(), name='comment-list'),
    #url(r'^notesapp(?P<pk>[0-9]+)/comment/(?P<ck>[0-9]+)/$', views.CommentDetail.as_view(), name='comment-detail'),
    url(r'^users/$', views.UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),
    url(r'^$', 'notesapp.views.api_root'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
