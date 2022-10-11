from django.contrib import admin
from .models import *
from django.apps import apps

# Register your models here.

admin.site.register(SentMessage)
