#!/usr/bin/env python
#coding=utf-8

from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.core.urlresolvers import get_script_prefix
from django.http import HttpResponseRedirect
from django.contrib.sites.models import RequestSite
from django.shortcuts import redirect
from mail import send_mail_with_new_pack

import biplist

from models import App, Package, ProvisioningProfile
from forms import *


def get_host(request):
    site_name = RequestSite(request).domain
    full_url = request.build_absolute_uri()
    url_scheme = full_url.split("://")[0]
    print(request.build_absolute_uri())
    host = url_scheme + "://" + site_name
    return host


def appstore(request):
    return render(request, "Application/appstore.html")


# @login_required
def app_list(request):
    #return render(request, "Application/appstore.html")
    apps = App.objects.all()
    provs = ProvisioningProfile.objects.all()
    upload_file_form = UploadFileForm()

    host = get_host(request)
    # host = request.get_host()

    return render(request, "Application/app_list.html",
                  {'apps': apps, 'provs': provs, 'host': host, 'form': upload_file_form},
                  context_instance=RequestContext(request))
    # return render(request, "Application/app_list.html", context_instance=RequestContext(request))


# @login_required
def app_detail(request, app_id):
    app = App.objects.get(id=app_id)
    packages = Package.objects.filter(app_id=app_id)

    upload_file_form = UploadFileForm()

    host = get_host(request)
    # host = request.get_host()

    return render(request, "Application/app_detail.html",
                  {'app': app, "packages": packages, 'form': upload_file_form})


def app_packages_list(request, app_id):
    packs = Package.objects.filter(app_id=app_id)
    # print(packs)
    # print type(packs)
    return render(request, "Application/package_list.html", {'packs': packs})


def ota_plist(request):
    params = request.GET
    package_id = params.get("pack_id")
    package = Package.objects.get(id=package_id)

    host = get_host(request)
    # host = get_host(request)
    print(host)
    response = render(request, "Application/distribution.plist", {'package': package, "host": host},
                      content_type="text/xml")
    return response


# handle file upload
def package_upload(request):
    if request.method == 'GET':
        upload_file_form = UploadFileForm()
        return render(request, "Application/upload_file.html", {'form': upload_file_form})
    elif request.method == 'POST':
        upload_file_form = UploadFileForm(request.POST, request.FILES)
        print(upload_file_form)
        p = upload_file_form.save(commit=False)
        print(p)
        p.parse_ipa
        print("pack:" + p.bundle_name)
        app = App.objects.get_or_create(app_identifier=p.bundle_identifier)[0]
        print("r", app.id)
        print("r", app.app_name)
        print(type(app.app_name))
        if app.app_name is None or len(app.app_name) == 0:
            print("good condition")
            app.app_name = p.bundle_name
        app.save()
        p.app = app
        p.save()
        return redirect("app_detail", app.id)


# Test JQuery upload file
def pack_upload2(request):
    if request.method == "GET":
        return render(request, "Application/picture_form.html")
    elif request.method == 'POST':
        return HttpResponse("Good")


def package_update(request):
    if request.method == 'POST':
        package = Package(request.POST)
        print(package)
        print("---------------------------------")
        package.bundle_identifier = request.POST.get("bundle_identifer", None)
        print(package)
        print("package")
        print("package.bundle_identifier")
        print(package.bundle_identifier)
        print(package.id)
        form = UpdatePackageForm(request.POST)
        return render(request, "Application/upload_success.html", context_instance=RequestContext(request))
    else:
        return HttpResponse("FAIL")


def provisioning_profile_list(request):
    provs = ProvisioningProfile.objects.all()[0]
    print(provs)
    plist = biplist.readPlist(provs.profile_path)
    print(plist)

    return HttpResponse("provisioning_profile_list")
