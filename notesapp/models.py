from django.db import models

# Create your models here.
class Note(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    owner = models.ForeignKey('auth.user')
 
    class Meta:
	    ordering = ('created',)

class Comment(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	body = models.TextField()
	owner = models.ForeignKey('auth.user')
	note = models.ForeignKey(Note, related_name='comments')
	
	class Meta:
	    ordering = ('created',)

