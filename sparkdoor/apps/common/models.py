"""
models.py - `common` app models module.
"""
import os
import binascii
from datetime import datetime

from django.db import models

from sparkdoor.apps.spark.models import Device


class DoorEvent(models.Model):
    """
    Timeseries data for events that are recorded by the door app.
    """
    OPEN_EVENT = 'open',
    USE_PASS_EVENT = 'use_pass'
    EVENTS = (
        (OPEN_EVENT, 'open'),
        (USE_PASS_EVENT, 'use pass')
    )

    device = models.ForeignKey(Device)
    time = models.DateTimeField(auto_now=True)
    event = models.CharField(max_length=50, blank=False, choices=EVENTS)
    event_data = models.TextField(blank=True)


class DoorPass(models.Model):
    """
    Acts as a shareable invite with expiration and/or finite-use rules
    for allowing an anonymous user to operate a door app device.
    """
    token = models.CharField(max_length=40, primary_key=True)
    device = models.ForeignKey(Device)
    expires_at = models.DateTimeField(null=True)
    use_limit = models.IntegerField(null=True)
    uses = models.IntegerField(default=0)

    def is_expired(self):
        """
        Test if this token is expired or not.
        """
        expired_date_reached = False
        use_limit_reached = False
        if self.expires_at:
            expired_date_reached = self.expires_at < datetime.now()
        if self.use_limit:
            use_limit_reached = self.uses >= self.use_limit
        return expired_date_reached or use_limit_reached

    def save(self, *args, **kwargs):
        """
        Add the token if not present.
        """
        if not self.token:
            self.token = self.generate_token()
        return super(self.__class__, self).save(*args, **kwargs)

    def generate_token(self):
        """
        Generate a random 20 character hex token.
        """
        return binascii.hexlify(os.urandom(20)).decode()


class IDCard(models.Model):
    """
    Stores RFID cards that can be registered with a door and used to
    open it.
    """
    uid = models.CharField(max_length=10, blank=False)
    device = models.ForeignKey(Device)
    name = models.CharField(max_length=100)
