from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from notesapp.models import Note
from notesapp.serializers import NoteSerializer

class JSONResponse(HttpResponse):
    # An HttpResponse that renders its content into JSON

    def __init__(self, data, **kwargs):
	content = JSONRenderer().render(data)
	kwargs['content_type'] = 'application/json'
	super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def note_list(request):
    # List all notes, or create a new note

    if request.method == 'GET':
	notes = Note.objects.all()
	serializer = NoteSerializer(notes, many=True)
	return JSONResponse(serializer.data)

    elif request.method == 'POST':
	data = JSONParser().parse(request)
	serializer = NoteSerializer(data=data)
	if serializer.isvalid():
	    serializer.save()
	    return JSONResponse(serializer.data, status=201)
	return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def note_detail(request, pk):
    # Retrieve, update or delete a note 
    try:
	note = Note.objects.get(pk=pk)
    except Note.DoesNotExist:
	return HttpResponse(status=404)

    if request.method == 'GET':
	serializer = NoteSerializer(note)
	return JSONResponse(serializer.data)

    elif request.method == 'POST':
	data = JSONParser().parse(request)
	serializer = NoteSerializer(note, data=data)
	if serializer.is_valid():
	    serializer.save()
	    return JSONResponse(serializer.data)
	return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
	note.delete()
	return HttpResponse(status=204)

