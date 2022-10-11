from django.contrib import admin
from django.urls import path
from .views import message, message_desk, send_email_msg
urlpatterns = [
    path('message/', message, name="message"),
    path('message_desk/', message_desk, name="message_desk"),
    path('send_email_msg/', send_email_msg, name="send_email_msg"),
    # path('base/', base, name="base"),
]
