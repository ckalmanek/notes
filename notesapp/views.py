from rest_framework import status
from rest_framework import renderers
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics
from rest_framework import permissions
from notesapp.models import Note
from notesapp.models import Comment
from notesapp.serializers import NoteSerializer
from notesapp.permissions import IsOwnerOrReadOnly
from notesapp.serializers import CommentSerializer
from django.http import Http404
from django.contrib.auth.models import User
from notesapp.serializers import UserSerializer

class NoteList(generics.ListCreateAPIView):
    # List all notes, or create a new note

    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    						IsOwnerOrReadOnly,)

    def pre_save(self, obj):
        obj.owner = self.request.user   

class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    # Retrieve, update or delete a note 

    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    						IsOwnerOrReadOnly)

    def pre_save(self, obj):
    	obj.owner = self.request.user

class CommentList(generics.ListCreateAPIView):
    # List all commments associated with a note, or create a new commment

    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = []
        notekey = self.kwargs['pk']
        try:
            note = Note.objects.get(pk=notekey)
        except Note.DoesNotExist:
            return queryset
        queryset = Comment.objects.filter(note=note)
        return queryset

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, 
                            IsOwnerOrReadOnly)

    def pre_save(self, obj):
        obj.owner = self.request.user
        notekey = self.kwargs['pk']
        obj.note = Note.objects.get(pk=notekey)


class CommentRUD(generics.RetrieveUpdateDestroyAPIView):
    # Retrieve, update or delete a note 

    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = []
        notekey = self.kwargs['pk']
        commentkey = self.kwargs['ck']
        try:
            note = Note.objects.get(pk=notekey)
        except Note.DoesNotExist:
            return queryset
        queryset = Comment.objects.filter(note=note)
        return queryset


    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                            IsOwnerOrReadOnly)

    def pre_save(self, obj):
        obj.owner = self.request.user
        notekey = self.kwargs['pk']
        obj.note = Note.objects.get(pk=notekey)

class UserList(generics.ListAPIView):
    # List all users
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly)


class UserDetail(generics.RetrieveAPIView):
    # Retrieve a user
	queryset = User.objects.all()
	serializer_class = UserSerializer
	# pemission_classes = (permissions.IsAuthenticatedOrReadOnly,)

@api_view(('GET',))
def api_root(request, format=None):
	return Response({
		'users': reverse('user-list', request=request, format=format),
		'notesapp': reverse('note-list', request=request, format=format)
	})


