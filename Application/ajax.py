#!/usr/bin/env python
#coding=utf-8

__author__ = 'ryan'

from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

@dajaxice_register
def sayhello(request):
    return simplejson.dumps({'message':'Hello World'})
