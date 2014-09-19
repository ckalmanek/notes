from django.db import models

class Tag(models.Model):
	body = models.TextField()

	def __unicode__(self):
		return '%d: %s' % (self.pk, self.body)

class Note(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    owner = models.ForeignKey('auth.user')
    tags = models.ManyToManyField(Tag)
 
    class Meta:
    	ordering = ('created',)

    def __unicode__(self):
    	return '%d: %s' % (self.pk, self.body)

class Comment(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	body = models.TextField()
	owner = models.ForeignKey('auth.user')
	note = models.ForeignKey(Note, related_name='comment')
	comment_id = models.AutoField(primary_key=True)
	
	class Meta:
		ordering = ('created',)

	def __unicode__(self):
		return '%d: %s' % (self.comment_id, self.body)

