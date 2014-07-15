from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from notesapp.models import Note
from notesapp.serializers import NoteSerializer
from notesapp.permissions import IsOwnerOrReadOnly
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

class UserList(generics.ListAPIView):
    # List all users
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    # Retrieve a user
	queryset = User.objects.all()
	serializer_class = UserSerializer

