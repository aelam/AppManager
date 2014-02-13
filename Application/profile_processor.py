#!/usr/bin/env python
#coding=utf-8

__author__ = 'ryan'

import plistlib
import sys

PLIST_START_MARKER = '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">'
PLIST_END_MARKER = '</plist>'




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
