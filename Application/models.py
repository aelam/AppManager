from django.db import models


class App(models.Model):
#    app_identifier = models.CharField(max_length=60)
    app_name = models.CharField(max_length=60)

    def __unicode__(self):
        return ( self.app_name)

class Package(models.Model):
    version = models.CharField(max_length=60)
    create_at = models.DateTimeField(auto_now_add=True)
    app = models.ForeignKey(App)
    ipa_path = models.FileField(upload_to ='apps/')
#    release_note = models.TextField()

    def __unicode__(self):
        return "%s-%s " %(self.app,self.version)


    def get_path(self):
        return "apps/%s/%s/" % (self.app.app_name,self.version)

    def generate_manifest(self):
        return ""

    def get_app_bundle(self):
        return ""


# Create your models here.
class Comment(models.Model):
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    package = models.ForeignKey(Package)

    def __unicode__(self):
        return self.content