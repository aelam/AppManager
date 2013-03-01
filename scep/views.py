# Create your views here.

# /enroll
# /checkin
# /scep?operation=GetCACert&message=EnrollmentCAInstance
# /scep?operation=GetCACaps&message=EnrollmentCAInstance
# /scep?operation=PKIOperation&message=MII.....AAA
# /checkin
# /scep?operation=GetCACert&message=EnrollmentCAInstance
# /scep?operation=GetCACaps&message=EnrollmentCAInstance
# /scep?operation=PKIOperation&message=MII.....AAA

from django.http import HttpResponse
from django.shortcuts import get_object_or_404,render
from django.views.decorators.csrf import csrf_exempt

from mdm.models import Device, Topic

# @csrf_exempt
def main(request):
    print(request.method)
    if request.POST:
        print(request)
        print request['POST']
        return HttpResponse("GOOD")
    else:
        # print(request)
        response = render(request, "cert/CA.mobileconfig",content_type='application/x-apple-aspen-config')
        # response = render(request, "mdm/mdm.plist", content_type='application/x-apple-aspen-config')
        # return HttpResponse(a, content_type="application/xhtml+xml")
        return response

def enroll(request):
    return HttpResponse("enroll")

def checkin(request):
    return HttpResponse("CheckIn")

def scep(request):
    print(request.method)
    if request.POST:
        print(request)
        print request['POST']
        return HttpResponse("GOOD")
    else:
        # print(request)
        response = render(request, "cert/CA.mobileconfig",content_type='application/x-apple-aspen-config')
        # response = render(request, "mdm/mdm.plist", content_type='application/x-apple-aspen-config')
        # return HttpResponse(a, content_type="application/xhtml+xml")
        return response

def main(request):
   return HttpResponse("main")


# def ca(request):
#     return HttpResponse("CA")
#     return render(request, "mdm/ca.pem", content_type="application/x-x509-ca-cert")