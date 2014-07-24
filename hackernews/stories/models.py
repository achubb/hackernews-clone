from urlparse import urlparse

from django.db import models
from django.contrib.auth.models import User

class Story(models.Model):
	title = models.CharField(max_length=200)
	url = models.URLField()
	points = models.IntegerField(default=1)
	moderator = models.ForeignKey(User, related_name='moderated_stories')# Pointer to Users Table
	voters = models.ManyToManyField(User, related_name='liked_stories')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	# Make a Read Only Propery called domain
	@property
	def domain(self):
		# Parse the url with the urlparse function (imported above)
		# Get the domain, in this case this is just .netloc
		# Then return this.
		return urlparse(self.url).netloc

	def __unicode__(self):
		return self.title

	class Meta:
		verbose_name_plural = "stories"
		# This is here to correct the plural spelling of stories in the admin.