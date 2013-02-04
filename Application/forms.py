#!/usr/bin/env python
#coding=utf-8

__author__ = 'ryan'
from django import forms
from django.forms import ModelForm,Textarea
from models import App,Comment,Package

class UploadFileForm(forms.Form):
    file  = forms.FileField()


class PackageForm(ModelForm):
    class Meta:
        model = Package

class UpdatePackageForm(ModelForm):
    readonly_fields = ('id','ipa_path',)
#    id = forms.CharField(label="id",widget=forms.HiddenInput())
#    ipa_path = forms.FileField(widget=forms.HiddenInput())

    release_note = forms.Textarea()
    class Meta:
        model = Package
        exclude = ('ipa_path','version',"app")
#        fields = ('release_note',id,)
#        widgets = {
#            'id':
#            'release_note': Textarea(attrs={'cols': 80, 'rows': 20}),
#        }



class AppForm(ModelForm):
    class Meta:
        model = App

