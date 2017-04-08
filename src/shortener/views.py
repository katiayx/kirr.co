from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, Http404
from django.views import View

from analytics.models import ClickEvent

from .forms import SubmitUrlForm
from .models import KirrURL

class HomeView(View):
    def get(self, request, *args, **kwargs):
        the_form = SubmitUrlForm()
        context = {
            "title": "Kirr.co",
            "form": the_form,
        }
        return render(request, "shortener/home.html", context)

    def post(self, request, *args, **kwargs):
        
        form = SubmitUrlForm(request.POST) #passing in form data
        context = {
            "title": "Kirr.co",
            "form": form,
        }
        template = "shortener/home.html"

        if form.is_valid():
            new_url = form.cleaned_data.get("url")
            obj, created = KirrURL.objects.get_or_create(url=new_url)
            context = {
                "object": obj,
                "created": created,
            }
            if created:
                template = "shortener/success.html"
            else:
                template = "shortener/already-exists.html"
        
        return render(request, template, context) 

def kirr_redirect_view(request, shortcode=None, *args, **kwargs): #function based view
    #PAGE NOT FOUNT
    obj = get_object_or_404(KirrURL, shortcode=shortcode)#yello is field name, white is passed arg
    return HttpResponseRedirect(obj.url)

class URLRedirectView(View): #class based views, must specify method
    def get(self, request, shortcode=None, *args, **kwargs):
        qs = KirrURL.objects.filter(shortcode__iexact=shortcode)
        if qs.count() != 1 and not qs.exists():
            raise Http404
        obj = qs.first()
        # obj = get_object_or_404(KirrURL, shortcode=shortcode)
        print (ClickEvent.objects.create_event(obj))
        return HttpResponseRedirect(obj.url)




"""
def kirr_redirect_view(request, shortcode=None, *args, **kwargs): #function based view


    #PAGE NOT FOUNT
    obj = get_object_or_404(KirrURL, shortcode=shortcode)#yello is field name, white is passed arg
    obj_url = obj.url

    RAISES EXCEPTION IS INPUT SHORTCODE DOESN'T EXIST
    try:
        obj = KirrURL.objects.get(shortcode=shortcode)
    except:
        obj = KirrURL.objects.all().first()
    try/except handles all exceptions in the same way

    ANOTHER WAY TO HANDLE NON-EXISTANT SHORTCODE
    obj_url = None
    #query set is created only if input shortcode matches stored shortcode exactly
    qs = KirrURL.objects.filter(shortcode__iexact=shortcode.upper())
    #if qs (shortcode) even exists, and count is 1 (all should be unique)
    if qs.exists() and qs.count() == 1:
        #then grab the first from the query set
        obj = qs.first()
        obj_url = obj.url

    return HttpResponse("hello {sc}".format(sc=obj_url))

"""
