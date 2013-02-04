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

class App(models.Model):
#    app_identifier = models.CharField(max_length=60)
    app_name = models.CharField(max_length=60)

    def __unicode__(self):
        return ( self.app_name)

class Package(models.Model):
    app = models.ForeignKey(App)

    version = models.CharField(max_length=60)
    create_at = models.DateTimeField(auto_now_add=True)
    ipa_path = models.FileField(upload_to ='apps/',editable=False)
    release_note = models.TextField(null=True,blank=True)

    def __unicode__(self):
        return "%s-%s " %(self.app,self.version)

#    def save(self, force_insert=False, force_update=False, using=None):
#        self.create_at = datetime()
#        super.save(self,force_insert,force_insert,using)

    @staticmethod
    def handle(ipa):
        print(ipa)
        if ipa:
            package = Package(ipa_path=ipa)
            print "ipa = %s" % type(ipa)
            if type(ipa) == TemporaryUploadedFile:
                temp = ipa.temporary_file_path()
                print(ipa.size)
                print(ipa.name)
                print(temp)
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
#                print (zip.extract(info_path))
                #print os.getcwd()
                print(info_path)
                print(ipa.temporary_file_path)
                print("------")
                temp = os.path.dirname(temp)
                print(temp)
                print(zip.extract(info_path,temp))


            return package
        else:
            return None

    def get_app_bundle(self):
        return ""


# Create your models here.
class Comment(models.Model):
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    package = models.ForeignKey(Package)

    def __unicode__(self):
        return self.content

class ProvisioningProfile(models.Model):
    profile_path = models.FileField(upload_to="profiles")

