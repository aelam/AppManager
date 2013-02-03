#!/usr/bin/env python
#coding=utf-8

__author__ = 'ryan'

from django.utils import simplejson

def last_version(request,app_id):
    return simplejson.dumps({'message':'Hello World'})
