"""
WSGI config for InnerAppStore project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os, sys

import site

# Add the site-packages of the chosen virtualenv to work with


CURRENT_PATH = os.path.dirname(__file__)
PROJECT_PATH = os.path.dirname(CURRENT_PATH)

app_env = os.path.join(PROJECT_PATH, "app_env")
site_packages = os.path.join(app_env, 'lib/python2.7/site-packages')

sys.path.append(PROJECT_PATH)
sys.path.append(CURRENT_PATH)


site.addsitedir(site_packages)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "InnerAppStore.settings")


# Activate your virtual env
activate_this = os.path.join(app_env, "bin/activate_this.py")
activate_env=os.path.expanduser(activate_this)
execfile(activate_env, dict(__file__=activate_env))

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
