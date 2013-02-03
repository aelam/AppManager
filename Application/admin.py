__author__ = 'ryan'


from django.contrib import admin
from models import App,Package,Comment


admin.site.register(App)
admin.site.register(Package)
admin.site.register(Comment)