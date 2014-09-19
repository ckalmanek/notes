from django.forms import widgets
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import reverse
from notesapp.models import Note
from notesapp.models import Comment
from notesapp.models import Tag

class NoteSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.Field(source='owner.username')
    comment = serializers.RelatedField(many=True)
    tags = serializers.RelatedField(many=True)

    class Meta:
        model = Note
        fields = ('url', 'owner', 'body', 'comment', 'tags')

class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.Field(source='owner.username')
    note = serializers.HyperlinkedRelatedField(read_only=True,
                                                view_name='note-detail')

    class Meta:
        model = Comment
        fields = ('comment_id', 'owner', 'body', 'note')

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')

class TagSerializer(serializers.ModelSerializer):

    def validate_body(self, attrs, source):
        # check that tag is not already defined
        value = attrs[source]
        queryset = Tag.objects.filter(body=value)
        print queryset
        if queryset.count() > 0:
            raise serializers.ValidationError("Tag already exists")
        return attrs

    class Meta:
        model = Tag
        fields = ('id', 'body')
