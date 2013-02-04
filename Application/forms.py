#!/usr/bin/env python
#coding=utf-8

__author__ = 'ryan'
from django import forms
from django.forms import ModelForm,Textarea,TextInput,FileInput
from models import App,Comment,Package

class UploadFileForm(forms.Form):
    file  = forms.FileField()


class PackageForm(ModelForm):
    class Meta:
        model = Package

class UpdatePackageForm(ModelForm):

    class Meta:
        model = Package
        exclude = ('version',"app")
        widgets = {
            'release_note': Textarea(attrs={'cols': 80, 'rows': 20}),
            'bundle_identifer':TextInput(attrs={'readonly':True}),
            'bundle_name':TextInput(attrs={'readonly':True}),
            'bundle_version':TextInput(attrs={'readonly':True}),
            'bundle_short_version':TextInput(attrs={'readonly':True}),

        }



class AppForm(ModelForm):
    class Meta:
        model = App

