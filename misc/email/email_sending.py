# -*- coding: utf-8 -*-
import codecs
import os

import mandrill as mandrill
from flask import render_template_string
from eventbus.queue_deferred import queue_deferred

MANDRILL_API_KEY = ''
MANDRILL_EMAIL_FROM_NAME = ''

mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)

MANDRILL_MAX_NON_ASYNC_RECIPIENTS = 1000
EMAIL_TEMPLATE_DIR = 'path/to/template/folder'


def send_emails_via_mandrill(from_email, from_name, to_emails, subject, cc_emails=None, html=None, text=None,
                             headers=None, preserve_recipients=False):
    """
    Reference : https://mandrillapp.com/api/docs/messages.python.html#method=send

    :param from_email: From email
    :param from_name: Name of from email
    :param to_emails: List of emails to send
    :param subject: Email subject
    :param cc_emails: List of emails to be cc
    :param html: Email body htmlx
    :param text: Email body text
    :param headers: Email headers
    :param preserve_recipients: When sending messages to multiple recipients in a single API call, if you do not want
    them to see each other’s information, set the preserve_recipients option to false.
    :return: Mail sending result
    """

    if len(to_emails) > MANDRILL_MAX_NON_ASYNC_RECIPIENTS:
        raise Exception('Number of emails to send exceeds limit')

    if not headers:
        headers = {}

    to_emails = [{'email': email} for email in to_emails]

    if cc_emails is not None:
        cc_emails = [{'email': email, 'type': 'cc'} for email in cc_emails]
        to_emails += cc_emails

    try:
        message = {
            'from_email': from_email,
            'from_name': from_name,
            'to': to_emails,
            'subject': subject,
            'html': html,
            'text': text,
            'headers': headers,
            'preserve_recipients': preserve_recipients
        }

        result = mandrill_client.messages.send(message=message)
        return result

    except mandrill.Error as e:
        raise e


def send_email_via_mandrill(from_email, from_name, to_email, subject, html=None, text=None, headers=None,
                            preserve_recipients=False):
    to_emails = [to_email]
    return send_emails_via_mandrill(from_email, from_name, to_emails, subject,
                                    html=html, text=text, headers=headers, preserve_recipients=preserve_recipients)


def send_emails_with_template(from_email, from_name, to_emails, subject, template, headers=None, cc_emails=None,
                              preserve_recipients=False, **template_args):
    """
    Send emails using template
    :param from_email:
    :param from_name: Name of from email
    :param to_emails:
    :param subject:
    :param template: Template file name
    :param headers:
    :param cc_emails: List of emails to be cc
    :param preserve_recipients: Whether recipients can see others information if the email is send to multiple
    recipients.
    :param template_args: Arguments in the template
    :return: Mail sending result
    """
    # Generate path to template file
    template_path = os.path.join(EMAIL_TEMPLATE_DIR, template)

    with codecs.open(template_path, 'r', 'utf-8') as f:
        # Get the content of template and replace arguments with values
        html = f.read()
        html = render_template_string(html, **template_args)

    return send_emails_via_mandrill(from_email, from_name, to_emails, subject, html=html, headers=headers,
                                    cc_emails=cc_emails, preserve_recipients=preserve_recipients)


def queue_sending_email(from_email, to_email, subject, body):
    to_emails = [to_email]

    queue_sending_emails(from_email, to_emails, subject, body)


def queue_sending_emails(from_email, to_emails, subject, body):
    queue_deferred(
        send_emails_via_mandrill,
        from_email=from_email,
        from_name=MANDRILL_EMAIL_FROM_NAME,
        to_emails=to_emails,
        subject=subject,
        text=body,
        _queue='default',
    )


def queue_sending_emails_with_template(**kwargs):
    queue_deferred(
        send_emails_with_template,
        _queue='default', **kwargs
    )
