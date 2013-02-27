import plistlib

from django.http import HttpResponse
from django.shortcuts import get_object_or_404,render
from django.views.decorators.csrf import csrf_exempt

from mdm.models import Device, Topic

@csrf_exempt
def main(request):


    # a = '''
    # <?xml version="1.0" encoding="UTF-8"?>
    # <!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    # <plist version="1.0">
    # <dict>
    # </dict>
    # </plist>
    # '''
    response = render(request, "mdm/mdm.plist", content_type='application/x-apple-aspen-config')
    # return HttpResponse(a, content_type="application/xhtml+xml")
    return response

@csrf_exempt
def checkin(request):
    """
    A device will send one of three different type of message in the MDM Check-in protocol:

    a) Authenticate: Sent when a device is enrolling for MDM.
    b) TokenUpdate: A device is informing the server its token has changed.
    c) Checkout: he device is unenrolling from MDM.

    """

    plist = plistlib.readPlistFromString(request.raw_post_data)
    topic_name = plist.get('Topic')
    topic = Topic.objects.filter(name=topic_name)
    topic = topic.get() if bool(topic) else None

    message_type = plist.get('MessageType')
    uuid = plist.get('UDID')
    if message_type == 'Authenticate':
        # Determine whether the device is eligble for MDM
        device, created = Device.objects.get_or_create(udid=uuid)
        if topic is not None:
            topic.devices.add(device)
    elif message_type == 'TokenUpdate':
        device, created = Device.objects.get_or_create(udid=uuid)
        device.token = plist.get('Token').asBase64()
        device.push_magic = plist.get('PushMagic')
        device.unlock_token = plist.get('UnlockToken').asBase64()
        device.save()
    elif message_type == 'Checkout':
        device = get_object_or_404(Device, uuid=uuid)
        if topic is not None:
            topic.devices.remove(device)

    return HttpResponse(plistlib.writePlistToString({}), mimetype='text/xml')
