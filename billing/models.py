from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Card(models.Model):
	data = models.CharField(max_length=500)
	user = models.ForeignKey(User, on_delete=models.PROTECT)
	num = models.CharField(max_length=4)
	
	@property
	def display_number(self):
		return u'xxxx-xxxx-xxxx-' + unicode(self.num)
	
	def __unicode__(self):
		return unicode(self.user.username) + ' - ' + self.display_number
