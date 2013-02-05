#!/usr/bin/env python
#coding=utf-8
#
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
import biplist
import zipfile,re


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


    def test_biplist(self):
        plist = biplist.readPlist("/Users/ryan/Desktop/pytest/Info.plist")

        print(plist)
        print plist.get(r'CFBundleName',None)
        print plist.get(r'CFBundleVersion',None)
        print plist.get(r'CFBundleShortVersionString',None)

        icons = plist.get(r'CFBundleIcons',None)
        primaryIcon = icons.get(r"CFBundlePrimaryIcon",None)
        CFBundleIconFile = primaryIcon.get(r"CFBundleIconFiles",None)[0]
        print(CFBundleIconFile)

        print(type(icons))

    def test_re(self):
        print "HELLO:"
        zip = zipfile.ZipFile("/Users/ryan/Desktop/fiveStar/FiveStar.zip",'r')
        #    valid = re.compile(r"^payload\/*(\w+).app\/info.plist")
        #    valid = re.compile(r"^payload")
        #    for name in zip.namelist():
        #        if valid.match(name):
        #            print "YAY"
        # print name

        l = (
            "Payload/1231231.app/Info.plist",
            "Payload/123 1231.app/Info.plist",
            "Payload/23中33文.app/Info.plist",
            "Payload/23中33文.app/Info.plist",
            "Payload/12 3.app/1231.app/Info.plist",
            "Payload/123.app/1231.app/Info.plist",
            "Payload/app/.app/Info.plist",
            )


        valid = re.compile(r"^Payload\/[^\/]+.app\/Info.plist$",re.IGNORECASE)
        for i in l:
            m = valid.match(i)
            if m:
                print m.group()
            else:
                print "None:" + i


    def testList(self):
        icons = ["1","2"]
        print icons.count(0)

