from django.forms import widgets
from django.contrib.auth.models import User
from rest_framework import serializers
from notesapp.models import Note
from notesapp.models import Comment

class NoteSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.Field(source='owner.username')
    comments = serializers.HyperlinkedRelatedField(many=True, read_only=True, 
                                                    required=False,
                                                    view_name='comment-detail')

    class Meta:
        model = Note
        fields = ('url', 'owner', 'body', 'comments')

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.Field(source='owner.username')
    note = serializers.HyperlinkedRelatedField(read_only=True,
                                                view_name="note-detail")

    class Meta:
        model = Comment
        fields = ('owner', 'body')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    # notes = serializers.PrimaryKeyRelatedField(many=True)
    notes = serializers.HyperlinkedRelatedField(many=True, view_name='notes-list')

    class Meta:
        model = User
        fields = ('url', 'username')
