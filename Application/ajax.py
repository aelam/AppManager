#!/usr/bin/env python
#coding=utf-8

__author__ = 'ryan'

from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

@dajaxice_register
def oldPackages(request):
    # return simplejson.dump({"message":"app_previous_versions"})
    return simplejson.dumps({'message':'oldPackages'})
