#!/usr/bin/env python
#coding=utf-8
#

from zipfile import ZipFile
import re
import os
import tempfile
import shutil
import uuid
import plistlib
import string

from django.db import models
import biplist
from django.contrib.auth.models import User

from InnerAppStore import settings
import ipin

PLIST_START_MARKER = '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">'
PLIST_END_MARKER = '</plist>'


class ProvisioningProfile(models.Model):
    profile_path = models.FileField(upload_to="profiles")

    applicationIdentifierPrefix = models.CharField(max_length=100, editable=False)
    create_at = models.DateTimeField(editable=False, auto_now_add=True, blank=True)
    application_identifier = models.CharField(max_length=100, editable=False, null=True)
    name = models.CharField(max_length=100, editable=False, null=True)
    provisionsAllDevices = models.BooleanField(default=False, editable=False)
    expirationDate = models.DateTimeField(editable=False, null=True)
    UUID = models.CharField(max_length=100, editable=False, null=True)

    PROFILE_TYPE_CHOICES = (
        ("DEBUG", "debug"),
        ("AD-HOC", "ad-hoc"),
        ("APPSTORE", "appstore"),
    )
    profile_type = models.CharField(max_length=100, choices=PROFILE_TYPE_CHOICES, default="DEBUG")


    def ProfileToPlist(profile_path):
    # print(profile_path)
        with open(profile_path, "rb") as provisioning_file:
            file_contents = provisioning_file.read()

        plist_start = file_contents.find(PLIST_START_MARKER)
        plist_end = file_contents.find(PLIST_END_MARKER)
        if plist_start < 0 or plist_end < 0:
            return None

        plist_end += len(PLIST_END_MARKER)

        plist_dict = plistlib.readPlistFromString(file_contents[plist_start:plist_end])

        # print(plist_dict)
        print plist_dict["DeveloperCertificates"]
        return plist_dict


class App(models.Model):
    app_identifier = models.CharField(max_length=60, unique=True)
    app_name = models.CharField(max_length=60)
    app_store_id = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return u"%s" % self.app_name


class Package(models.Model):
    app = models.ForeignKey(App)

    create_at = models.DateTimeField(auto_now_add=True)
    ipa_path = models.FileField(upload_to='apps/')

    bundle_identifier = models.CharField(max_length=60, blank=True, null=True)

    bundle_name = models.CharField(max_length=100, blank=True, null=True)
    display_name = models.CharField(max_length=100, blank=True, null=True)
    bundle_version = models.CharField(max_length=100, blank=True, null=True)
    bundle_short_version = models.CharField(max_length=100, blank=True, null=True)

    icon_path = models.FileField(upload_to='apps/icons', editable=False, null=True)
    big_icon_path = models.FileField(upload_to='apps/icons', editable=False, null=True)

    release_note = models.TextField(null=True, blank=True)

    #TODO
    provision = models.ForeignKey(ProvisioningProfile, null=True, blank=True)

    def __unicode__(self):
        return "%s-%s" % (self.bundle_version, self.create_at)

    class Meta:
        ordering = ['-create_at', 'bundle_short_version']

    def install_link(self):
        return None

    #TODO find icons
    @property
    def parse_ipa(self):
        if self.ipa_path is None:
            return None
        ipa = ZipFile(self.ipa_path, 'r')
        print ipa
        nameList = ipa.namelist()

        # regex for find Info.Plist location and unzip it
        # then we also can find the icons paths
        re_info = re.compile(r"^Payload/[^/]+.app/Info.plist$", re.IGNORECASE)

        for name in nameList:
            match = re_info.match(name)
            if match:
                info_path = name
                break
        if info_path is None:
            return None

        tempfd = tempfile.gettempdir()
        real_info_path = ipa.extract(info_path, tempfd)
        plist = biplist.readPlist(real_info_path)

        self.bundle_identifier = plist.get("CFBundleIdentifier", None)
        self.bundle_name = plist.get(r'CFBundleName', None)
        self.bundle_version = plist.get(r'CFBundleVersion', None)
        self.bundle_short_version = plist.get(r'CFBundleVersion', None)
        self.display_name = plist.get(r"CFBundleDisplayName", None)

        icons = plist.get(r'CFBundleIcons', None)
        icons__ = []
        if icons:
            primary_icon = icons.get(r"CFBundlePrimaryIcon", None)
            icons__ = primary_icon.get(r"CFBundleIconFiles", None)
        else:
            icons = plist.get(r"CFBundleIconFiles", None)
            if icons:
                icons__ = icons

        print(icons__)
        if len(icons__) > 0:
            print("icons__.count(0) > 0")
            random_str = str(uuid.uuid4())
            dst_icon_name = random_str + ".png"
            dst_big_icon_name = random_str + "_2x.png"
            index = 0

            for icon_name_ in icons__:
                if index > 2:
                    break
                icon_name_ = string.replace(icon_name_, ".png", "")
                icon_name_ += "@2x.png"
                icon_path = os.path.join(os.path.dirname(info_path), icon_name_)
                print "icon_path" + icon_path
                dst_icon_dir = os.path.dirname(real_info_path)
                try:
                    dst_icon_path = ipa.extract(icon_path, dst_icon_dir)
                except KeyError:
                    print "KeyError"
                    continue

                if len(dst_icon_path) == 0:
                    return

                dst_dir = os.path.join(settings.MEDIA_ROOT, "apps", "icons")
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                if index == 0:
                    media_dst_path = os.path.join(dst_dir, dst_icon_name)
                    print "dst_icon_path : " + dst_icon_path
                    print "media_dst_path : " + media_dst_path
                    ipin.updatePNG(dst_icon_path)
                    shutil.copy2(dst_icon_path, media_dst_path)
                    self.icon_path = os.path.join("apps", "icons", dst_icon_name)
                    index += 1
                elif index == 1:
                    media_dst_path = os.path.join(dst_dir, dst_big_icon_name)
                    print "dst_icon_path : " + dst_icon_path
                    print "media_dst_path : " + media_dst_path
                    ipin.updatePNG(dst_icon_path)
                    shutil.copy2(dst_icon_path, media_dst_path)
                    self.big_icon_path = os.path.join("apps", "icons", dst_big_icon_name)


        ipa.close()

        return self.bundle_identifier


class Comment(models.Model):
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    package = models.ForeignKey(Package)

    def __unicode__(self):
        return self.content


class Device(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    nick = models.CharField(max_length=100, blank=True)


class Team(models.Model):
    team_name = models.CharField(max_length=100)
    team_token = models.CharField(max_length=100)
    owner = models.ForeignKey(User, related_name="owner")
    members = models.ManyToManyField(User, null=True)

    def __unicode__(self):
        return self.team_name


