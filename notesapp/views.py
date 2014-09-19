from rest_framework import status
from rest_framework import parsers
from rest_framework import renderers
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics
from rest_framework import permissions
from notesapp.models import Note
from notesapp.models import Comment
from notesapp.models import Tag
from notesapp.serializers import NoteSerializer
from notesapp.permissions import IsOwnerOrReadOnly
from notesapp.serializers import CommentSerializer
from notesapp.serializers import TagSerializer
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

    parser_classes = (parsers.JSONParser,)

    def pre_save(self, obj):
    	obj.owner = self.request.user

    def post_save(self, obj, created):
        print obj
        try: 
            tagstr = self.request.DATA['tags'][0]
            print tagstr
            queryset = Tag.objects.filter(body=tagstr)
            tag = queryset.first()
            print tag
            print obj
            obj.tags.add(tag)
        except Exception as inst:
            print type(inst)

class CommentListAll(generics.ListAPIView):
    # List all commments 

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, 
                            IsOwnerOrReadOnly)

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

class CommentInstance(generics.RetrieveUpdateDestroyAPIView):
    # Retrieve, update or delete a comment 

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()    

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                            IsOwnerOrReadOnly)

    def pre_save(self, obj):
        obj.owner = self.request.user

class TagList(generics.ListCreateAPIView):
    # List all tags associated with a note, or create a new tag

    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Tag.objects.all()


class TagInstance(generics.RetrieveUpdateDestroyAPIView):
    # Retrieve, update or delete a tar 

    serializer_class = TagSerializer
    queryset = Tag.objects.all()    

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

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


