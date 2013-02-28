#!/usr/bin/env python
#coding=utf-8

__author__ = 'ryan'

from django.http import HttpResponse, HttpResponseRedirect

def main(request):

    redirect = request.path + "app"

    return HttpResponseRedirect(redirect)

