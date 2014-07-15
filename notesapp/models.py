from django.db import models

# Create your models here.
class Note(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    owner = models.ForeignKey('auth.user', related_name='notesapp')

    class Meta:
	ordering = ('created',)
