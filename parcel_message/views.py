import datetime

import httpx
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string

from .models import SentMessage


# Create your views here.

def message(request):
    return render(request, "parcel_message\\message.html")


async def message_desk(request):
    if request.method == 'POST':
        form_input = request.POST
        email = form_input['email']
        password = form_input['password']
        api_url = f"http://localhost:7000/parcel_backends/desk_login_ext/{email}/{password}/"
        status = ""
        context = {}
        if email == "" or password == "":
            return render(request, "parcel_message\\message.html", {"error": "Enter all Fields"})
        else:
            try:
                async with httpx.AsyncClient() as client:
                    login_staff = await client.post(api_url)
                    if login_staff.status_code == httpx.codes.OK:
                        raw_login = login_staff.json()
                        print(raw_login)
                        login_status = raw_login['status']
                        if login_status == "success":
                            login_data = raw_login['data']
                            status = login_status
                            context = login_data
                        elif login_status == "error":
                            login_data = raw_login['data']
                            status = login_status
                            context = login_data
            except httpx.RequestError as ex:
                print(f"An error occurred while requesting {ex.request.url!r}.")
        if status == "success":
            return render(request, "parcel_message\\message_desk.html", context)
        elif status == "error":
            return render(request, "parcel_message\\message.html", {"error": login_data})


def send_email_msg(request):
    if request.method == 'POST':
        form_input = request.POST
        sender = form_input['sender']
        raw_recipients = form_input['recipients']
        recipients = raw_recipients.split(',')
        subject = form_input['subject']
        html_body = form_input['html_body']
        body = form_input['body']
        if sender == "" or raw_recipients == "" or subject == "" or (body == "" and html_body == ""):
            return render(request, "parcel_message\\message_desk.html", {"error": "Enter all Fields"})
        else:
            message_body = None
            if html_body == "":
                message_body = body
            else:
                set_body = "parcel_message\\" + html_body
                message_body = render_to_string(set_body)
            email_operation = EmailMessage(subject, message_body, from_email=sender, to=recipients)
            email_operation.send(fail_silently=False)
            save_msg = SentMessage(sender=sender, recipient=raw_recipients, subject=subject,
                                   body=message_body, sent_at=f"{datetime.datetime.today()}")
            save_msg.save()
            ctx = {
                "detail": "Message sent successfully!"
            }
            return render(request, "parcel_message\\message_desk.html", ctx)



