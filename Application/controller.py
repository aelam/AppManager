#from coffin.shortcuts import render_to_response
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext
import os.path
from django import http
from django.http import HttpResponseRedirect, HttpResponse

from Application.file_manager import FileManager


def box(request):
    fm = FileManager(request.user.username)
    if request.method =="GET":
        return render_to_response("files.html", {"username":request.user.username, 
                                                 "files": fm.get_files()}, 
                                                context_instance = RequestContext(request))
    
    if request.method =="POST":
        if "delete" in request.GET:
            filename = request.GET["delete"]
            fm.delete_file(filename)
            return HttpResponse(content = ('{"result":"ok"}'))
            
        
        filename = request.GET["file"]
        data = request.raw_post_data
        name = fm.save_file(filename, data)
        return HttpResponse(content = ('{"file":"%s"}' % name))
