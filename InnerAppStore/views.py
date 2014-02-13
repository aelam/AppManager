#!/usr/bin/env python
#coding=utf-8

__author__ = 'ryan'

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import resolve

def main(request):
    # print resolve("app")
    redirect = request.path + "app"
#    str = "{{MEDIA_URL}} {{STATIC_URL}} {{SCRIPT_URL}}"

    # return HttpResponse(str)
    # return render()
    # return render(request, "Application/Test.html")
    return HttpResponseRedirect(redirect)

