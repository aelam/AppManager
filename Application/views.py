# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from models import App,Comment,Package
#from coffin.shortcuts import render_to_response
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext
from django.core.context_processors import csrf

import os.path
from django import http
from django.http import HttpResponseRedirect, HttpResponse

from Application.file_manager import FileManager
import uuid

from ajax import sayhello

def app_list(request):
    apps = App.objects.all()
    return render(request,"Application/app_list.html",{'apps':apps})

def app_detail(request,app_id):
    print app_id
    app = App.objects.get(id = app_id)
    packages = Package.objects.filter(app_id = app_id)
    print(app)

#    ipa_url = settings.SERVER_URL+"/app/install"

    return render(request,"Application/app_detail.html",{'app':app, "packages":packages})


def app_packages_list(request,app_id):
    packs = Package.objects.filter(app_id=app_id)
    print(packs)
    print type(packs)
    return render(request,"Application/package_list.html",{'packs':packs})

def package_list(request):
    print request.GET
    packs = Package.objects.all() #(app_id=app_id)
    return render(request,"Application/package_list.html",{'packs':packs})

def ota_plist(request):
    params = request.GET
    package_id = params.get("pack_id")
    package = Package.objects.get(id=package_id)
    response = render(request,"Application/distribution.plist",content_type="text/xml")
    return response

def get_version(request,app_id):
    return ""


def upload(request):
    if request.method == 'GET':
        return render(request,"Application/upload_file.html")
    elif request.method == 'POST':
        handle_uploaded_file(request.FILES.get("filename"))
        return render(request,"Application/upload_file.html",context_instance=RequestContext(request))



def handle_uploaded_file(f):
    filename = str(uuid.uuid1()) + '.ipa'
    path = os.path.join(settings.MEDIA_ROOT,"cache",filename)
    print "path: %s " % path
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()

    return path

#def upload(request):
#    fm = FileManager(request.user.username)
#    if request.method =="GET":
#        return render_to_response("Application/files.html", {"username":request.user.username,
#                                                 "files": fm.get_files()},
#            context_instance = RequestContext(request))
#
#    if request.method =="POST":
#        if "delete" in request.GET:
#            filename = request.GET["delete"]
#            fm.delete_file(filename)
#            return HttpResponse(content = ('{"result":"ok"}'))
#
#
#        filename = request.GET["file"]
#        data = request.raw_post_data
#        name = fm.save_file(filename, data)
#        return HttpResponse(content = ('{"file":"%s"}' % name))
