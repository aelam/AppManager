__author__ = 'ryan'


def base_url(request):
    """
    Return a BASE_URL template context for the current request.
    """
    if request.is_secure():
        scheme = 'https://'
    else:
        scheme = 'http://'

    return {'BASE_URL': scheme + request.get_host(),
            'PROJECT_BASE_URL': scheme + request.get_host() + request.META['SCRIPT_NAME'],
    }
