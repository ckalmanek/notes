from django.forms import widgets
from django.contrib.auth.models import User
from rest_framework import serializers
from notesapp.models import Note

class NoteSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.Field(source='owner.username')

    class Meta:
        model = Note
        fields = ('url', 'owner', 'body')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    # notes = serializers.PrimaryKeyRelatedField(many=True)
    notes = serializers.HyperlinkedRelatedField(many=True, view_name='notes-detail')

    class Meta:
        model = User
        fields = ('url', 'username', 'notesapp')
