from django.forms import widgets
from rest_framework import serializers
from notesapp.models import Note

class NoteSerializer(serializers.Serializer):
    pk = serializers.Field()
    body = serializers.CharField(widget=widgets.Textarea, max_length=100000)

    def restore_object(self, attrs, instance=None):
	"""
	Create or update a new Note instance, given a dictionary attrs
	of deserialized field values.
	"""
	if instance:
	    # Update existing instance
	    instance.body = attrs.get('body', instance.body)
	    return instance

	# Create new Note
	return Note(**attrs)

