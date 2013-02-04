#!/usr/bin/env python
#coding=utf-8

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

from django.core.files.uploadedfile import InMemoryUploadedFile,TemporaryUploadedFile
import os.path
from django import http
from django.http import HttpResponseRedirect, HttpResponse
from forms import PackageForm,AppForm

from forms import *
import uuid

from ajax import sayhello

def app_list(request):
    apps = App.objects.all()
    upload_file_form = UploadFileForm()

    return render(request,"Application/app_list.html",{'apps':apps, 'form':upload_file_form})

def app_detail(request,app_id):
    print app_id
    app = App.objects.get(id = app_id)
    packages = Package.objects.filter(app_id = app_id)

    upload_file_form = UploadFileForm()

    return render(request,"Application/app_detail.html",{'app':app, "packages":packages,'form':upload_file_form})


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


# handle file upload
def package_upload(request):
    if request.method == 'GET':
        upload_file_form = UploadFileForm()
        return render(request,"Application/upload_file.html",{'form':upload_file_form})
    elif request.method == 'POST':
        upload_file_form = UploadFileForm(request.POST, request.FILES)
        if upload_file_form.is_valid():
            print("upload_file_form.is_valid")
        print(request.FILES['file'])
        file = request.FILES['file']
        package = Package.handle(file)
        if package is None:
            print ":( failed"
        else:
            print(package.ipa_path)
            print('awesome upload success')

        packageForm = UpdatePackageForm(instance=package)

        return render(request,"Application/upload_success.html",{"package":package,"form":packageForm}, context_instance=RequestContext(request))

def package_update(request):
    if request.method == 'POST':
        package = Package(request.POST)
        print(package.ipa_path)
        print(package.id)
        return render(request,"Application/upload_success.html", context_instance=RequestContext(request))
    else:
        return HttpResponse("FAIL")



def handle_uploaded_file(f):
    folder = os.path.join(settings.MEDIA_ROOT,"app")
    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = str(uuid.uuid1()) + '.ipa'
    path = os.path.join(folder,filename)
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
