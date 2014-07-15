from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from notesapp.models import Note
from notesapp.serializers import NoteSerializer
from django.contrib.auth.models import User
# from notesapp.serializers import UserSerializer

@api_view(['GET', 'POST'])
def note_list(request, format=None):
    # List all notes, or create a new note

    if request.method == 'GET':
	    notes = Note.objects.all()
	    serializer = NoteSerializer(notes, many=True)
	    return Response(serializer.data)

    elif request.method == 'POST':
    	# how does request.user get passed to the Note constructor?
	    serializer = NoteSerializer(data=request.DATA)
	    if serializer.is_valid():
	        serializer.save()
	        return Response(serializer.data, status=status.HTTP_201_CREATED)
	    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'DELETE'])
def note_detail(request, pk, format=None):
    # Retrieve, update or delete a note 
    try:
	    note = Note.objects.get(pk=pk)
    except Note.DoesNotExist:
	    return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
	    serializer = NoteSerializer(note)
	    return Response(serializer.data)

    elif request.method == 'POST':
	    serializer = NoteSerializer(note, data=request.DATA)
	    if serializer.is_valid():
	        serializer.save()
	        return Response(serializer.data)
	    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
	    note.delete()
	    return Response(status=status.HTTP_204_NO_CONTENT)
"""
@api_view(['GET'])
def user_list(request, format=None):
    # List all users
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def user_detail(request, pk, format=None):
    # Retrieve a user
	user = User.objects.all()
	serializer = UserSerializer(user)
	return Response(serializer.data)
"""
