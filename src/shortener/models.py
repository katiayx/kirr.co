from __future__ import unicode_literals
from django.conf import settings #import Configuration settings
from django.db import models

from django_hosts.resolvers import reverse

from .validators import validate_url, validate_dot_com
from .utils import code_generator, create_shortcode


SHORTCODE_MAX = getattr(settings, "SHORTCODE_MAX", 15) #looking for "SHORTCODE_MAX" in settings,
#if not there, set it -- good when reusing the app

#SHORTCODE_MAX = settings.SHORTCODE_MAX ok as well

class KirrURLManager(models.Manager):
    """model manager handles logic behind the model
    redefine methods to suit the project

    once redefined, must link to class KirrURL below
    """

    def all(self, *args, **kwargs):
        """redefine all method"""
        qs_main = super(KirrURLManager,self).all(*args, **kwargs)
        qs = qs_main.filter(active=True)
        return qs

    def refresh_shortcodes(self, items=100):
        """custom model manager to refresh all shortcodes at once"""

        qs = KirrURL.objects.filter(id__gte=1)
        if items is not None and isinstance(items, int):
            qs = qs.order_by('-id')[:items] #reverse order from beginning all the way up to items arg
            # could also do ''-url' reverse alphabetically
        new_codes = 0 #creating a count
        for q in qs: #qs is a list of codes
            q.shortcode = create_shortcode(q)
            print(q.id)
            q.save()
            new_codes += 1
        return "New codes made: {i}".format(i=new_codes)


class KirrURL(models.Model):
    url         = models.CharField(max_length=220, validators=[validate_url, validate_dot_com])
    shortcode   = models.CharField(max_length=SHORTCODE_MAX, unique=True, blank=True)
    updated     = models.DateTimeField(auto_now=True)#evertime the model is saved
    timestamp   = models.DateTimeField(auto_now_add=True)#when model was created
    active      = models.BooleanField(default=True)
    #empty_datetime = models.DateTimeField(auto_now=False, auto_now_add=False)

    #link to model manager
    objects = KirrURLManager()

    def save(self, *args, **kwargs): #for any args or key-word-arg
        """overriding default save method"""
        if self.shortcode is None or self.shortcode == '': #don't need to reset shortcode everytime
            self.shortcode = create_shortcode(self)
        if not "http" in self.url: 
            self.url = "http://" + self.url #reset url to include http://, if none included in input
        super(KirrURL,self).save(*args,**kwargs)#calling save method

    def __str__(self):
        return str(self.url)
        # self.pk = primary key auto-field
        # self.id is an alt = same as pk

    def __unicode__(self):
        return str(self.url)

    def get_short_url(self):
        """can just template variable to object.get_short_url"""
        url_path = reverse('scode', kwargs={'shortcode': self.shortcode}, host='www', scheme='http')
        #kwargs shortcode is coming from urls.py name urlpattern
        return url_path