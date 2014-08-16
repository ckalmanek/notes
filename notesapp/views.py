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
        #queryset = Comment.objects.all()
        pk = self.kwargs['pk']
        note = Note.objects.get(pk=pk)
        note_url = "http://127.0.0.1:8000/notesapp/" + str(pk)
        print note_url
        queryset = Comment.objects.filter(note=note)
        return queryset

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, 
                            IsOwnerOrReadOnly)

    def pre_save(self, obj):
        obj.owner = self.request.user
        print self.request
        obj.note = Note.objects.get(pk=1)


class CommentRUD(generics.RetrieveUpdateDestroyAPIView):
    # Retrieve, update or delete a note 

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                            IsOwnerOrReadOnly)

    def pre_save(self, obj):
        obj.owner = self.request.user
        #obj.note = Note.objects.get(pk=1)

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


