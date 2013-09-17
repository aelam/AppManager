#!/usr/bin/env python
#coding=utf-8

__author__ = 'ryan'

from django.utils import simplejson
# from django.core.serializers import serialize
# from django.utils.simplejson import dumps, loads, JSONEncoder
# from django.db.models.query import QuerySet
# from django.utils.functional import curry
from models import App
from django.http import HttpResponseRedirect, HttpResponse
# from django.utils import simplejson
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers


def last_version(request,app_id):
    return simplejson.dumps({'message':'Hello World'})


def apps(request):
    apps = App.objects.select_related().all()
    apps_json = serializers.serialize("json", apps)
    return HttpResponse(apps_json, mimetype='application/json')
