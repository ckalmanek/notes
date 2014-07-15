from django.forms import widgets
from django.contrib.auth.models import User
from rest_framework import serializers
from notesapp.models import Note

class NoteSerializer(serializers.Serializer):
    pk = serializers.Field()
    body = serializers.CharField(widget=widgets.Textarea, max_length=100000)
    owner = serializers.Field(source='owner.username')

    def restore_object(self, attrs, instance=None):
    # Create or update a new Note instance, given a dictionary attrs of deserialized field values.

        if instance:
            # Update existing instance
            instance.body = attrs.get('body', instance.body)
            # instance.owner = attrs.get('owner', instance.owner)
            return instance

		# Create new Note
        return Note(**attrs)

        class Meta:
            model = Note
            fields = {'body'}
			# fields = ('owner', 'body')

class UserSerializer(serializers.ModelSerializer):
    notes = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'notesapp')
