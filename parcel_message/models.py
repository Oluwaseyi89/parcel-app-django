from django.db import models
import datetime


# Create your models here.

class SentMessage(models.Model):
    sender = models.CharField(default="WebMaster@parcel_app.com", max_length=100)
    recipient = models.TextField(max_length=2000)
    subject = models.CharField(max_length=200)
    body = models.TextField(max_length=4000)
    sent_at = models.CharField(default=f"{datetime.datetime.today()}", max_length=100)

    def __str__(self):
        return self.subject
