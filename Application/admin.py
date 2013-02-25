__author__ = 'ryan'


from django.contrib import admin
from models import App, Package, Comment, ProvisioningProfile


admin.site.register(App)
admin.site.register(Package)
admin.site.register(Comment)



class ProvisioningProfileAdmin(admin.ModelAdmin):
    fields = ('profile_path',)


admin.site.register(ProvisioningProfileAdmin)