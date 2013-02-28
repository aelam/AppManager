#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ryan'

# -*- coding: utf-8 -*-

# /enroll
# /checkin
# /scep?operation=GetCACert&message=EnrollmentCAInstance
# /scep?operation=GetCACaps&message=EnrollmentCAInstance
# /scep?operation=PKIOperation&message=MII.....AAA
# /checkin
# /scep?operation=GetCACert&message=EnrollmentCAInstance
# /scep?operation=GetCACaps&message=EnrollmentCAInstance
# /scep?operation=PKIOperation&message=MII.....AAA


from django.conf.urls import url, patterns

urlpatterns = patterns('scep.views',
                       url(r'^scep$', 'scep'),
                       url(r'^enroll/?$', 'enroll', name='scep-enroll'),
                       url(r'^checkin/?$', 'checkin'),

                       )
