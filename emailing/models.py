from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save

from .utilities import MailchimpEmailing

class EmailingPreferences(models.Model):
    user                   = models.OneToOneField(settings.AUTH_USER_MODEL)
    subscribed             = models.BooleanField(default=True)
    mailchimp_subscribed   = models.NullBooleanField(blank=True)
    mailchimp_message      = models.TextField(null=True, blank=True)
    timestamp              = models.DateTimeField(auto_now_add=True)
    updated                = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

def emailing_pref_reciever_create(sender, instance, created, *args, **kwargs):
    if created:
        status_code, response_data = MailchimpEmailing().subscribe_user(instance.user.email)
        print(status_code, response_data)

post_save.connect(emailing_pref_reciever_create, sender=EmailingPreferences)


def emailing_pref_reciever_update(sender, instance, *args, **kwargs):
    if instance.subscribed != instance.mailchimp_subscribed:
        if instance.subscribed:
            status_code, response_data = MailchimpEmailing().subscribe_user(instance.user.email)

        else:
            status_code, response_data = MailchimpEmailing().unsubscribe_user(instance.user.email)

        if response_data['status'] == 'subscribed':
            instance.subscribed = True
            instance.mailchimp_subscribed = True
            instance.mailchimp_message = response_data
        else:
            instance.subscribed = False
            instance.mailchimp_subscribed = False
            instance.mailchimp_message = response_data

pre_save.connect(emailing_pref_reciever_update, sender=EmailingPreferences)


def make_emailing_pref_reciever(sender, instance, created, *args, **kwargs):
    if created:
        EmailingPreferences.objects.get_or_create(user=instance)

post_save.connect(make_emailing_pref_reciever, sender=settings.AUTH_USER_MODEL)
