from django.db import models


class Device(models.Model):
    name = models.CharField(max_length=255)
    udid = models.CharField(max_length=255, unique=True)
    identifier = models.CharField(max_length=255, unique=True)
    push_magic = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    unlock_token = models.TextField()


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)
    devices = models.ManyToManyField(Device, related_name='topics')


class DeviceGroup(models.Model):
    pass


class ProvisioningProfile(models.Model):
    pass


class Application(models.Model):
    pass


class ConfigurationProfile(models.Model):
    topic = models.ForeignKey(Topic)


class MDMPayload(object):
    """
    * id_cert_uuid (required)
        - IdentityCertificate-UUID (str)
        - UUID of the certificate payload for the device's identity. It may also point to a SCEP payload.
    * topic (required)
        - Topic (str)
        - The topic that MDM listens to for push notifications. The certificate that the server uses to
          send push notifications must have the same topic in its subject. The topic must begin with the com.apple.mgmt. prefix.
    * server_url (required)
        - ServerURL (str)
        - The URL that the device contacts to retrieve device management instructions.
          Must begin with the https:// URL scheme, and may contain a port number
    * sign_message (optional)
        - SignMessage (bool)
        - If true, each message coming from the device carries the additional Mdm-Signature HTTP header. Defaults to false.
    * checkin_url (optional)
        -  CheckInURL (str)
        -  The URL that the device should use to check in during installation. Must begin with the https:// URL scheme
           and may contain a port number (:1234, for example). If this URL is not given, the ServerURL is used
           for both purposes.
    * checkout_on_removal (optional)
        - CheckOutWhenRemoved (bool)
        -  If true, the device attempts to send a CheckOut message to the check-in server when the profile is removed.
           Defaults to false.
    * access_rights (required)
        - AccessRights (int, flags)
        - ...
    * use_development_apns (optional)
        - UseDevelopmentAPNS (bool)
        - If true, the device uses the development APNS servers. Otherwise, the device uses the production servers.
          Defaults to false.
    """
    payload_type = 'com.apple.mdm'
    version = 1
    identifier = 'A value must be provided.'
    uuid = 'A globally unique value must be provided.'
