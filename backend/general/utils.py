from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from general.email_content import MESSAGE_CONTENT
from general.sms import TiwilioClient
import threading


def get_custom_message_content(message_number):
    content = MESSAGE_CONTENT.get(message_number, {})
    return content


def get_protocol_domain():
    domain = Site.objects.get_current().domain
    return 'https', domain,


def email_sending(message_code, to_emails, data_for_subject=None, data_for_template=None):
    if data_for_subject:
        if not data_for_template:
            data_for_template = {}
        data_for_template.update(data_for_subject)
    else:
        data_for_subject = {}
    message = get_custom_message_content(message_code)
    subject = message.get('subject', '').format(**data_for_subject)
    template = message.get('template', '')
    protocol, domain = get_protocol_domain()
    message = render_to_string(template, {
        'data_for_template': data_for_template,
        'protocol': protocol,
        'domain': domain
    })

    if isinstance(to_emails, str):
        to_emails = [to_emails]

    email = EmailMessage(
        subject, message, to=to_emails, from_email=settings.DEFAULT_FROM_EMAIL
    )
    email.content_subtype = 'html'
    email.send()


def send_email(message_code, to_emails, data_for_subject=None, data_for_template=None):
    threading.Thread(target=email_sending, args=(message_code, to_emails, data_for_subject, data_for_template),
                     name="SEND_EMAIL").start()


def send_sms(phone, text):
    threading.Thread(target=TiwilioClient().send_text_message, args=(str(phone), text),
                     name="SEND_SMS").start()


def send_support_email(issue_type, data):
    if issue_type == 'ISSUE_IN_FUNDING':
        send_email("ISSUE_IN_FUNDING", settings.SUPPORT_EMAIL,
                   data_for_template={'issue_loans': data})
