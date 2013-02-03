#!/usr/bin/env python
#coding=utf-8

__author__ = 'ryan'

from django.core.files.uploadhandler import FileUploadHandler
from django.core.cache import cache
import time

class LogFileUploadHandler(FileUploadHandler):
    def __init__(self, request=None):
        super(LogFileUploadHandler, self).__init__(request)
        if 'formhash' in self.request.GET:
            self.formhash = self.request.GET['formhash']
            cache.add(self.formhash, {})
            self.activated =True
        else:
            self.activated = False

    def new_file(self, *args, **kwargs):
        super(LogFileUploadHandler, self).new_file(*args, **kwargs)
        if self.activated:
            fields = cache.get(self.formhash)
            fields[self.field_name] = 0
            cache.set(self.formhash, fields)


    def receive_data_chunk(self, raw_data, start):
    #        time.sleep(5) for local test, it slow down the upload speed
        if self.activated:
            fields = cache.get(self.formhash)
            fields[self.field_name] = start
            cache.set(self.formhash, fields)
        return raw_data

    def file_complete(self, file_size):
        if self.activated:
            fields = cache.get(self.formhash)
            fields[self.field_name] = -1
            cache.set(self.formhash, fields)

    def upload_complete(self):
        if self.activated:
            fields = cache.get(self.formhash)
            fields[self.formhash] = -1
            cache.set(self.formhash, fields)
