#!/usr/bin/env python
#coding=utf-8
#

from django.db import models
import datetime
from django.core.files.uploadedfile import TemporaryUploadedFile
from zipfile import ZipFile,LargeZipFile
import re,os
from django.core.files import temp as tempfile
from InnerAppStore import settings
#import plist_parser

import biplist
import shutil,uuid

class App(models.Model):
    app_identifier = models.CharField(max_length=60,unique=True)
    app_name = models.CharField(max_length=60)

    def __unicode__(self):
        return ( self.app_name)

class Package(models.Model):

#    def __init__(self, *args, **kwargs):
#        super(Package, self).__init__(*args, **kwargs)
#        self.bundle_identifer = kwargs.get(r"bundle_identifer",None)

    app = models.ForeignKey(App)

    version = models.CharField(max_length=60)
    create_at = models.DateTimeField(auto_now_add=True)
    ipa_path = models.FileField(upload_to ='apps/',editable=False)

    bundle_identifer = models.CharField(max_length=60,blank=True,null=True)

    bundle_name = models.CharField(max_length=100,blank=True,null=True)
    bundle_name = models.CharField(max_length=100,blank=True,null=True)
    bundle_version = models.CharField(max_length=100,blank=True,null=True)
    bundle_short_version = models.CharField(max_length=100,blank=True,null=True)

    icon_path = models.FileField(upload_to ='apps/icons',editable=False)

    release_note = models.TextField(null=True,blank=True)

    def __unicode__(self):
        return "%s-%s " %(self.bundle_identifer,self.version)

    @staticmethod
    def handle(ipa):
        if ipa:
            package = Package(ipa_path=ipa)
            if type(ipa) == TemporaryUploadedFile:
                temp = ipa.temporary_file_path()
                if ipa.name.endswith(".ipa") or ipa.name.endswith(".zip"):
                    print("good zipped file")
                else:
                    return None
                zip = ZipFile(temp,'r')
                nameList = zip.namelist()
                # find info.plist
                valid = re.compile(r"^Payload\/[^\/]+.app\/Info.plist$",re.IGNORECASE)
                for name in nameList:
                    match = valid.match(name)
                    if match:
                        info_path = name
                        break
                unzip_ipa_dir = os.path.dirname(temp)
                real_info_path = zip.extract(info_path,unzip_ipa_dir)

                plist = biplist.readPlist(real_info_path)

                package.bundle_identifer = plist.get("CFBundleIdentifier",None)
                package.bundle_name = plist.get(r'CFBundleName',None)
                package.bundle_version =  plist.get(r'CFBundleVersion',None)
                package.bundle_short_version =  plist.get(r'CFBundleVersion',None)

                icons = plist.get(r'CFBundleIcons',None)
                if icons:
                    primaryIcon = icons.get(r"CFBundlePrimaryIcon",None)
                    icon_name_ = primaryIcon.get(r"CFBundleIconFiles",None)[0]
                else:
                    icon_name_ = plist.get(r"CFBundleIconFiles",None)[0]

                icon_path = os.path.join(os.path.dirname(info_path),icon_name_)

                unzip_icon_dir = os.path.dirname(real_info_path)
                unzip_icon_path = zip.extract(icon_path,unzip_icon_dir)

                icon_name = str(uuid.uuid4()) + ".png"
                dst_dir= os.path.join(settings.MEDIA_ROOT,"apps/icons")
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                dst_path = os.path.join(dst_dir,icon_name)
                shutil.copy2(unzip_icon_path,dst_path)
                package.icon_path = dst_path

                app = App.objects.get_or_create(app_identifier=package.bundle_identifer)[0]
                app.app_name = package.bundle_name
                print(package.bundle_identifer)
                print(app)
                package.app = app

            return package
        else:
            return None


# Create your models here.
class Comment(models.Model):
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    package = models.ForeignKey(Package)

    def __unicode__(self):
        return self.content

class ProvisioningProfile(models.Model):
    profile_path = models.FileField(upload_to="profiles")

