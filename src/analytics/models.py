
from django.db import models

from shortener.models import KirrURL

class ClickEventManager(models.Manager):
	def create_event(self, kirr_instance):
		if isinstance(kirr_instance, KirrURL):
			#ClickEvent.objects = self
			#objects is called in ClickEvent -- which is calling ClickEventManager
			obj, created = self.get_or_create(kirr_url=kirr_instance)
			obj.count += 1
			obj.save()
			return obj.count
		return None

class ClickEvent(models.Model):
	#assoicate to URL
	kirr_url 	= models.OneToOneField(KirrURL)
	count 		= models.IntegerField(default=0)
	updated     = models.DateTimeField(auto_now=True)
	timestamp   = models.DateTimeField(auto_now_add=True)	

	objects = ClickEventManager()

	def __str__(self):
		return "{i}".format(i=self.count)
