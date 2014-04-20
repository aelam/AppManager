#!/usr/bin/env python
#coding=utf-8

__author__ = 'ryan'


from django.shortcuts import redirect
from django.http import HttpResponse


def main(request):
    # return HttpResponse("HELLO")
    return redirect("app_root")
