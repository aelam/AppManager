import base64
import datetime
from django.conf import settings
import os
import re


def create_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

class FileManager(object):
    
    def __init__(self, username):
        self.user = username
        self.dir =  os.path.join(settings.MEDIA_ROOT, "apps")
        create_dir(self.dir)
    
    def get_indexed_name(self, filename):
        if not os.path.exists(os.path.join(self.dir, filename)):
            return filename
        index = 1
        name, ext = os.path.splitext(filename)
        filename_regexp = "^(.*?)(_\d+)%s$" % ext.replace(".", "\.")
            
        match = re.match(filename_regexp, filename)
        if match:
            _index = int(match.group(2).replace('_', ''))
            name = match.group(1)
            index = _index+1
            
            
        new_name =  name + '_' + unicode(index)+ ext
        return self.get_indexed_name(new_name)
            
    
    def rename_file(self, filename):
        from pytils import translit

        filename = translit.translify(filename)
        
        filename = self.get_indexed_name(filename)
        return filename
        
    
    def save_file(self, filename, data):
        filename = self.rename_file(filename)
        
        file = open(os.path.join(self.dir, filename), 'w')
        file.write(data)
        file.close()
        
        return filename
    
    def delete_file(self, filename):
        os.remove(os.path.join(self.dir, filename))
        
        
    def get_files(self):
        return filter(lambda name: os.path.isfile(os.path.join(self.dir,name)), os.listdir(self.dir))