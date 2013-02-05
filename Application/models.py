#!/usr/bin/env python
#coding=utf-8
#

from django.db import models
import datetime
from django.core.files.uploadedfile import TemporaryUploadedFile
from zipfile import ZipFile
from InnerAppStore import settings
import re,os,tempfile,biplist,shutil,uuid


class App(models.Model):
    app_identifier = models.CharField(max_length=60,unique=True)
    app_name = models.CharField(max_length=60)

    def __unicode__(self):
        return u"%s" % ( self.app_name)

class Package(models.Model):

    app = models.ForeignKey(App)

    create_at = models.DateTimeField(auto_now_add=True)
    ipa_path = models.FileField(upload_to ='apps/')

    bundle_identifier = models.CharField(max_length=60,blank=True,null=True)

    bundle_name = models.CharField(max_length=100,blank=True,null=True)
    bundle_version = models.CharField(max_length=100,blank=True,null=True)
    bundle_short_version = models.CharField(max_length=100,blank=True,null=True)

    icon_path = models.FileField(upload_to ='apps/icons',editable=False,null=True)
    big_icon_path = models.FileField(upload_to ='apps/icons',editable=False,null=True)

    release_note = models.TextField(null=True,blank=True)

    def __unicode__(self):
        return "%s-%s " %(self.bundle_identifier,self.bundle_version)

    class Meta:
        ordering = ['-create_at', 'bundle_short_version']

    def parse_ipa(self):
        if self.ipa_path is None:
            return None
        zip = ZipFile(self.ipa_path,'r')
        nameList = zip.namelist()
        re_info = re.compile(r"^Payload\/[^\/]+.app\/Info.plist$",re.IGNORECASE)
        for name in nameList:
            match = re_info.match(name)
            if match:
                info_path = name
                break
        if info_path is None:
            return None

        tempfd = tempfile.gettempdir()
        real_info_path = zip.extract(info_path,tempfd)
        print(real_info_path)
        plist = biplist.readPlist(real_info_path)

        self.bundle_identifier = plist.get("CFBundleIdentifier",None)
        self.bundle_name = plist.get(r'CFBundleName',None)
        self.bundle_version =  plist.get(r'CFBundleVersion',None)
        self.bundle_short_version =  plist.get(r'CFBundleVersion',None)

        icons = plist.get(r'CFBundleIcons',None)
        icons__ = []
        if icons:
            primaryIcon = icons.get(r"CFBundlePrimaryIcon",None)
            icons__ = primaryIcon.get(r"CFBundleIconFiles",None)
        else:
            icons = plist.get(r"CFBundleIconFiles",None)
            if icons:
                icons__ = icons
        print("====================")
        print(icons__)
        if len(icons__) > 0:
            print("icons__.count(0) > 0")
            random_str = str(uuid.uuid4())
            dst_icon_name = random_str + ".png"
            dst_big_icon_name = random_str+"@2x.png"
            index = 0

            for icon_name_ in icons__:
                icon_path = os.path.join(os.path.dirname(info_path),icon_name_)
                print("icon_path "+ icon_path)
                dst_icon_dir = os.path.dirname(real_info_path)
                dst_icon_path = zip.extract(icon_path,dst_icon_dir)

                dst_dir= os.path.join(settings.MEDIA_ROOT,"apps/icons")
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                if index == 0:
                    media_dst_path = os.path.join(dst_dir,dst_icon_name)
                    shutil.copy2(dst_icon_path,media_dst_path)
                    self.icon_path = os.path.join("apps/icons",dst_icon_name)
                elif index == 1:
                    media_dst_path = os.path.join(dst_dir,dst_big_icon_name)
                    shutil.copy2(dst_icon_path,media_dst_path)
                    self.big_icon_path = os.path.join("apps/icons",dst_big_icon_name)
                print(media_dst_path)
                index = index+1

        zip.close()

        return self.bundle_identifier

    @staticmethod
    def handle(ipa):
        return None
        ipa = ""
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

                package.bundle_identifier = plist.get("CFBundleIdentifier",None)
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

